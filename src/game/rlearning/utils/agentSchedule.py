import random
import os
import math
import json
from bisect import bisect_left
from pathlib import Path



class AgentSchedule:
    def __init__(self, config):
        self.items = config.get("items", ["good_model.txt", "great_model.txt"])
        self.probs = config.get("probs", [0.3, 0.7])
        self.rng = random.Random(config.get("seed"))
        self.paths_cache = {}


    def _read_steps(self, path):
        path = Path(path)
        try:
            stat = path.stat()
        except FileNotFoundError:
            return []

        signature = (stat.st_mtime_ns, stat.st_size)
        cached = self.paths_cache.get(path)
        if cached is not None and cached[0] == signature:
            return cached[1]

        steps = []
        for line in path.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value.isascii() and value.isdecimal():
                steps.append(int(value))

        self.paths_cache[path] = (signature, steps)
        return steps

    @staticmethod
    def _available_steps(logdir):
        folder = Path(logdir) / "ckpt"
        steps = set()
        if not folder.is_dir():
            return steps

        for path in folder.glob("g_*"):
            value = path.name[2:]
            if not value.isascii() or not value.isdecimal():
                continue

            step = int(value)
            if step > 0 and path.is_file() and (folder / f"i_{step}").is_file():
                steps.add(step)

        return steps

    def get_restore_step(self, logdir, current_strength):
        available = self._available_steps(logdir)
        groups, weights = [], []

        for name, probability in zip(self.items, self.probs):
            if probability <= 0:
                continue

            steps = self._read_steps(Path(logdir) / name)
            candidates = [step for step in steps if step == 0 or step in available]
            if candidates:
                groups.append(candidates)
                weights.append(probability)

        if groups:
            candidates = self.rng.choices(groups, weights=weights, k=1)[0]
            return self.rng.choice(candidates)

        if available:
            return self.rng.choice(sorted(available))

        return 0



class BenchmarkGaussianSchedule(AgentSchedule):
    def __init__(self, config):
        self.candidate_list = config.get("candidate_list", "great_model.txt")
        super().__init__({
            "items": [self.candidate_list],
            "probs": [1.0],
            "seed": config.get("seed"),
        })

        self.benchmark_id = config["benchmark_id"]
        self.evaluation_dir = config.get("evaluation_dir", "evaluation")
        self.score_min = float(config["score_min"])
        self.score_max = float(config["score_max"])
        self.strength_offset = float(config.get("strength_offset", 0.0))
        self.sigma = float(config.get("sigma", 5.0))
        self.bin_width = float(config.get("bin_width", 2.0))
        self.report_cache = {}

        values = [self.score_min, self.score_max, self.strength_offset, self.sigma, self.bin_width]
        if not all(math.isfinite(value) for value in values):
            raise ValueError("分布参数必须是有限数值")
        if self.score_max <= self.score_min:
            raise ValueError("score_max 必须大于 score_min")
        if self.sigma <= 0 or self.bin_width <= 0:
            raise ValueError("sigma 和 bin_width 必须大于零")

    def _load_report_scores(self, logdir):
        folder = Path(logdir) / self.evaluation_dir
        files, signature = [], []

        for path in sorted(folder.glob("*.json")):
            try:
                stat = path.stat()
            except FileNotFoundError:
                continue

            files.append(path)
            signature.append((path.name, stat.st_mtime_ns, stat.st_size))

        signature = tuple(signature)
        cached = self.report_cache.get(folder)
        if cached is not None and cached[0] == signature:
            return cached[1]

        collected = {}
        for path in files:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (FileNotFoundError, json.JSONDecodeError):
                continue

            report = data.get("report", {})
            if report.get("benchmark_id") != self.benchmark_id:
                continue
            if report.get("valid") is not True or report.get("score") is None:
                continue

            try:
                step = int(report["step"])
                score = float(report["score"])
            except (KeyError, TypeError, ValueError):
                continue

            if step > 0 and math.isfinite(score) and 0 <= score <= 100:
                collected.setdefault(step, []).append(score)

        scores = {step: sum(values) / len(values) for step, values in collected.items()}
        self.report_cache[folder] = (signature, scores)
        return scores

    def _candidate_bins(self, logdir):
        scores = self._load_report_scores(logdir)
        evaluated_steps = sorted(scores)
        if not evaluated_steps:
            raise RuntimeError(f"{logdir} 没有 benchmark={self.benchmark_id} 的有效评测")

        available = self._available_steps(logdir)
        candidate_steps = sorted(set(self._read_steps(Path(logdir) / self.candidate_list)))
        bins = {}

        for step in candidate_steps:
            if step not in available:
                continue

            if step in scores:
                score = scores[step]
            else:
                index = bisect_left(evaluated_steps, step)
                if index == 0 or index == len(evaluated_steps):
                    continue

                left, right = evaluated_steps[index - 1], evaluated_steps[index]
                fraction = (step - left) / (right - left)
                score = scores[left] + fraction * (scores[right] - scores[left])

            bin_id = math.floor(score / self.bin_width)
            bins.setdefault(bin_id, []).append(step)

        if not bins:
            raise RuntimeError(f"{logdir} 没有可用且有评分的候选 checkpoint")
        return bins

    def get_restore_step(self, logdir, current_strength):
        strength = float(current_strength)
        if not math.isfinite(strength) or not 0 <= strength <= 1:
            raise ValueError("current_strength 必须位于 [0, 1]")

        position = max(0.0, min(1.0, strength + self.strength_offset))
        center = self.score_min + position * (self.score_max - self.score_min)

        bins = self._candidate_bins(logdir)
        bin_ids = sorted(bins)
        log_weights = []

        for bin_id in bin_ids:
            bin_center = (bin_id + 0.5) * self.bin_width
            distance = (bin_center - center) / self.sigma
            log_weights.append(-0.5 * distance * distance)

        maximum = max(log_weights)
        weights = [math.exp(value - maximum) for value in log_weights]
        chosen_bin = self.rng.choices(bin_ids, weights=weights, k=1)[0]
        return self.rng.choice(bins[chosen_bin])