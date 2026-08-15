from __future__ import annotations

import asyncio
import tempfile
import types
import unittest
from pathlib import Path

import httpx
import numpy as np

from game.rlearning.synthesis.artifacts import (
    write_reconstruction_artifact,
    write_transition_space_artifact,
)
from game.rlearning.synthesis.projection import pca_project_2d
from game.rlearning.synthesis_viewer.app import create_app
from game.rlearning.synthesis_viewer.repository import ArtifactRepository

try:
    import torch
    from game.rlearning.synthesis.state_space import (
        reconstruction_metrics,
        state_delta_from_target,
        state_from_prediction,
        state_from_target,
    )
    from game.rlearning.module.state_space.CVAE import CVAETrainer
except ModuleNotFoundError:
    torch = None


def _zone(cards: list[dict], slots: int = 10) -> dict:
    return {"card_count": len(cards), "slot_count": slots, "cards": cards}


def _state(life: int) -> dict:
    card_zones = {
        "hand": _zone(
            [
                {
                    "slot": 1,
                    "type": "Creature",
                    "mana_cost": [2, 1, 0, 0, 0, 0],
                    "attack": 2,
                    "health": 3,
                    "has_state": True,
                    "special_types": ["Flying"],
                    "presence_confidence": 1.0,
                }
            ]
        ),
        "library": _zone([], 40),
        "graveyard": _zone([], 40),
        "stack_cards": _zone([]),
    }
    board_zones = {"self_board": _zone([]), "oppo_board": _zone([])}
    return {
        "global_state": {
            "self_life": life,
            "oppo_life": 18,
            "mana": {"U": 0, "R": 0, "G": 0, "W": 3, "B": 0},
        },
        "card_zones": card_zones,
        "board_zones": board_zones,
    }


def _sample(sample_id: str = "000") -> dict:
    return {
        "schema_version": 1,
        "sample_id": sample_id,
        "source_index": 7,
        "summary": {"action": "Play hand card slot 1 (sub-action 0)", "score": 0.18},
        "metrics": {"global_mse": 0.03, "mask_bce": 0.15, "score": 0.18},
        "input_state": _state(20),
        "transition": {
            "card_used": {
                "description": "When this enters the battlefield, draw a card.",
                "type": "Creature",
                "mana_cost": [2, 1, 0, 0, 0, 0],
                "attack": 2,
                "health": 3,
                "has_state": True,
                "special_types": ["ETB effect"],
            },
            "action": {"index": 32, "label": "Play hand card slot 1 (sub-action 0)"},
        },
        "predicted_next_state": _state(19),
        "target_next_state": _state(20),
    }


class SynthesisViewerTest(unittest.TestCase):
    def test_artifact_is_discovered_and_rendered(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            experiment_dir = root / "ppo_white_v0"
            write_reconstruction_artifact(
                experiment_dir / "synthesis" / "2000",
                step=2000,
                samples=[_sample()],
            )

            repository = ArtifactRepository(root)
            self.assertEqual([item.name for item in repository.list_experiments()], ["ppo_white_v0"])
            self.assertEqual([item["step"] for item in repository.list_steps("ppo_white_v0")], [2000])

            response, step_page = asyncio.run(self._request_pages(create_app(root)))
            self.assertEqual(response.status_code, 200)
            self.assertIn("Predicted next state", response.text)
            self.assertIn("When this enters the battlefield", response.text)
            self.assertEqual(step_page.status_code, 200)
            self.assertIn("Reconstruction", step_page.text)

    @staticmethod
    async def _request_pages(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.get("/experiments/ppo_white_v0/2000/reconstruction/000")
            step_page = await client.get("/experiments/ppo_white_v0/2000")
        return response, step_page

    def test_transition_space_is_projected_linked_and_rendered(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            step_dir = root / "ppo_white_v0" / "synthesis" / "2000"
            write_reconstruction_artifact(
                step_dir,
                step=2000,
                samples=[_sample()],
            )

            mean_q = np.asarray(
                [
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                ],
                dtype=np.float32,
            )
            coordinates, projection = pca_project_2d(mean_q)
            vectors = {
                "mean_q": mean_q,
                "std_q": np.ones_like(mean_q),
                "mean_p": mean_q * 0.9,
                "std_p": np.ones_like(mean_q),
                "z_sampled": mean_q * 1.1,
            }
            records = [
                {
                    "vector_index": index,
                    "source_index": index * 10,
                    "is_highlighted": index == 1,
                    "reconstruction_sample_id": "000" if index == 1 else None,
                    "reconstruction_score": 0.18 if index == 1 else None,
                    "state_delta": {"change_type": "opponent_damage"},
                    "action": {"index": 32, "label": "Play hand card slot 1"},
                    "card_used": {
                        "type": "Creature",
                        "description": "Draw a card.",
                    },
                }
                for index in range(3)
            ]
            write_transition_space_artifact(
                step_dir,
                step=2000,
                vectors=vectors,
                records=records,
                coordinates=coordinates,
                projection=projection,
            )

            repository = ArtifactRepository(root)
            index, points = repository.transition_space("ppo_white_v0", 2000)
            self.assertEqual(index["point_count"], 3)
            self.assertEqual(index["highlight_count"], 1)
            self.assertEqual(len(points["points"]), 3)
            self.assertEqual(points["points"][1]["reconstruction_sample_id"], "000")

            response = asyncio.run(
                self._request_transition_page(create_app(root))
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("Transition space", response.text)
            self.assertIn("State change", response.text)
            self.assertIn("Highlight reconstruction samples", response.text)
            self.assertIn("/reconstruction/000", response.text)

    @staticmethod
    async def _request_transition_page(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            return await client.get(
                "/experiments/ppo_white_v0/2000/transition-space"
            )

    @unittest.skipIf(torch is None, "PyTorch is required for CVAE tensor conversion")
    def test_state_space_tensors_are_decoded_for_the_viewer(self) -> None:
        def target_zone(with_type: bool) -> dict:
            zone = {
                "card_mask": torch.tensor([[1.0, 0.0]]),
                "card_special_types": torch.zeros(1, 2, 11),
                "card_atks": torch.tensor([[0.10, 0.0]]),
                "card_hps": torch.tensor([[0.15, 0.0]]),
                "card_has_state": torch.tensor([[1.0, 0.0]]),
            }
            zone["card_special_types"][0, 0, 4] = 1.0
            if with_type:
                zone["card_types"] = torch.tensor([[1, 0]])
                zone["card_costs"] = torch.tensor([[[2.0, 1.0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]])
            return zone

        def prediction_zone(with_type: bool) -> dict:
            zone = {
                "card_mask": torch.tensor([[3.0, -3.0]]),
                "card_special_types": torch.zeros(1, 2, 11),
                "card_atks": torch.tensor([[0.10, 0.0]]),
                "card_hps": torch.tensor([[0.15, 0.0]]),
                "card_has_state": torch.tensor([[3.0, -3.0]]),
            }
            zone["card_special_types"][0, 0, 4] = 3.0
            if with_type:
                zone["card_types"] = torch.tensor([[[0.0, 3.0, 0.0, 0.0, 0.0], [3.0, 0.0, 0.0, 0.0, 0.0]]])
                zone["card_costs"] = torch.tensor([[[2.0, 1.0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]])
            return zone

        target = {
            "global_state": torch.tensor([[1.0, 0.9, 0.0, 0.0, 0.0, 0.15, 0.0]]),
            "card_zones": {name: target_zone(True) for name in ["hand", "library", "graveyard", "stack_cards"]},
            "board_zones": {name: target_zone(False) for name in ["self_board", "oppo_board"]},
        }
        source = {
            "global_state": torch.tensor([[1.0, 1.0, 0.0, 0.0, 0.0, 0.15, 0.0]]),
            "card_zones": {name: target_zone(True) for name in ["hand", "library", "graveyard", "stack_cards"]},
            "board_zones": {name: target_zone(False) for name in ["self_board", "oppo_board"]},
        }
        prediction = {
            "global_state": torch.tensor([[0.95, 0.9, 0.0, 0.0, 0.0, 0.1, 0.0]]),
            "card_zones": {name: prediction_zone(True) for name in ["hand", "library", "graveyard", "stack_cards"]},
            "board_zones": {name: prediction_zone(False) for name in ["self_board", "oppo_board"]},
        }

        decoded_target = state_from_target(target, 0)
        decoded_prediction = state_from_prediction(prediction, 0)
        delta = state_delta_from_target(source, target, 0)
        metrics = reconstruction_metrics(prediction, target, 0)

        self.assertEqual(decoded_target["global_state"]["self_life"], 20)
        self.assertEqual(decoded_target["card_zones"]["hand"]["cards"][0]["type"], "Creature")
        self.assertEqual(decoded_prediction["card_zones"]["hand"]["cards"][0]["attack"], 2)
        self.assertEqual(decoded_prediction["card_zones"]["hand"]["cards"][0]["health"], 3)
        self.assertEqual(delta["change_type"], "opponent_damage")
        self.assertIn("score", metrics)

    @unittest.skipIf(torch is None, "PyTorch is required for CVAE synthesis")
    def test_cvae_synthesis_batches_vectors_and_links_highlights(self) -> None:
        def target_zone(batch_size: int, with_type: bool, device) -> dict:
            zone = {
                "card_mask": torch.tensor([[1.0, 0.0]], device=device).repeat(batch_size, 1),
                "card_special_types": torch.zeros(batch_size, 2, 11, device=device),
                "card_atks": torch.tensor([[0.10, 0.0]], device=device).repeat(batch_size, 1),
                "card_hps": torch.tensor([[0.15, 0.0]], device=device).repeat(batch_size, 1),
                "card_has_state": torch.tensor([[1.0, 0.0]], device=device).repeat(batch_size, 1),
            }
            if with_type:
                zone["card_types"] = torch.tensor([[1, 0]], device=device).repeat(batch_size, 1)
                zone["card_costs"] = torch.tensor(
                    [[[2.0, 1.0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]],
                    device=device,
                ).repeat(batch_size, 1, 1)
            return zone

        def target_state(batch_size: int, device) -> dict:
            return {
                "global_state": torch.tensor(
                    [[1.0, 0.9, 0.0, 0.0, 0.0, 0.15, 0.0]],
                    device=device,
                ).repeat(batch_size, 1),
                "card_zones": {
                    name: target_zone(batch_size, True, device)
                    for name in ["hand", "library", "graveyard", "stack_cards"]
                },
                "board_zones": {
                    name: target_zone(batch_size, False, device)
                    for name in ["self_board", "oppo_board"]
                },
                "stack_extra": {
                    "player_one_hot": torch.zeros(batch_size, 2, 2, device=device),
                    "action_number": torch.zeros(
                        batch_size,
                        2,
                        dtype=torch.long,
                        device=device,
                    ),
                },
            }

        def prediction_zone(batch_size: int, with_type: bool, device) -> dict:
            zone = {
                "card_mask": torch.tensor([[3.0, -3.0]], device=device).repeat(batch_size, 1),
                "card_special_types": torch.zeros(batch_size, 2, 11, device=device),
                "card_atks": torch.tensor([[0.10, 0.0]], device=device).repeat(batch_size, 1),
                "card_hps": torch.tensor([[0.15, 0.0]], device=device).repeat(batch_size, 1),
                "card_has_state": torch.tensor([[3.0, -3.0]], device=device).repeat(batch_size, 1),
            }
            if with_type:
                card_types = torch.zeros(batch_size, 2, 5, device=device)
                card_types[:, 0, 1] = 3.0
                card_types[:, 1, 0] = 3.0
                zone["card_types"] = card_types
                zone["card_costs"] = torch.tensor(
                    [[[2.0, 1.0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]],
                    device=device,
                ).repeat(batch_size, 1, 1)
            return zone

        def prediction_state(batch_size: int, device) -> dict:
            return {
                "global_state": torch.tensor(
                    [[0.95, 0.9, 0.0, 0.0, 0.0, 0.1, 0.0]],
                    device=device,
                ).repeat(batch_size, 1),
                "card_zones": {
                    name: prediction_zone(batch_size, True, device)
                    for name in ["hand", "library", "graveyard", "stack_cards"]
                },
                "board_zones": {
                    name: prediction_zone(batch_size, False, device)
                    for name in ["self_board", "oppo_board"]
                },
            }

        class FakeDataset:
            def __init__(self):
                self.datas = [
                    {
                        "source_index": index,
                        "state": {
                            "card_used": {
                                "description": f"Card text {index}",
                                "special_type": [0.0] * 11,
                                "mana_cost": [0.1, 0, 0, 0, 0, 0],
                                "attack": 0.1,
                                "defend": 0.15,
                                "has_state": 1,
                                "card_type": 1,
                            }
                        },
                    }
                    for index in range(7)
                ]

            @staticmethod
            def get_sample(data):
                return data

            @staticmethod
            def collate_fn(samples):
                batch_size = len(samples)
                device = torch.device("cpu")
                return {
                    "source_indices": torch.tensor(
                        [sample["source_index"] for sample in samples],
                        dtype=torch.long,
                    ),
                    "action_index": torch.tensor(
                        [32 + sample["source_index"] for sample in samples],
                        dtype=torch.long,
                    ),
                    "state": target_state(batch_size, device),
                    "next_state": target_state(batch_size, device),
                }

        class FakeDecoder:
            def __call__(
                self,
                state_tokens,
                state_padding_mask,
                spans,
                transition_vec,
            ):
                return prediction_state(state_tokens.shape[0], state_tokens.device)

        def fake_encode(self, batch, models, isTrain, step, epoch):
            device = batch["action_index"].device
            source = batch["source_indices"].float().unsqueeze(1)
            offsets = torch.arange(4, device=device).float().unsqueeze(0)
            mean_q = source + offsets
            batch.update(
                {
                    "mean_q": mean_q,
                    "std_q": torch.ones_like(mean_q),
                    "mean_p": mean_q + 0.25,
                    "std_p": torch.ones_like(mean_q) * 1.1,
                    "z": mean_q + 0.5,
                    "tokens_s": torch.zeros(
                        mean_q.shape[0],
                        2,
                        4,
                        device=device,
                    ),
                    "pad_s": torch.zeros(
                        mean_q.shape[0],
                        2,
                        dtype=torch.bool,
                        device=device,
                    ),
                    "spans_s": {},
                }
            )
            return batch

        with tempfile.TemporaryDirectory() as temporary_directory:
            trainer = object.__new__(CVAETrainer)
            trainer.config = {
                "synthesis_transition_items": 5,
                "synthesis_items": 2,
                "synthesis_transition_batch_size": 2,
                "dataloader": {"batch_size": 2},
            }
            trainer.dataset = FakeDataset()
            trainer.models = {"TextEncoder": object()}
            trainer.rank = 0
            trainer.step = 2000
            trainer.epoch = 0
            trainer.logdir = temporary_directory
            trainer.encode = types.MethodType(fake_encode, trainer)

            trainer._synthesis(
                {"TokenTransitionStateDecoder": FakeDecoder()}
            )

            repository = ArtifactRepository(temporary_directory)
            index, points = repository.transition_space(
                Path(temporary_directory).name,
                2000,
            )
            self.assertEqual(index["point_count"], 5)
            self.assertEqual(index["highlight_count"], 2)
            highlighted = [
                point for point in points["points"] if point["is_highlighted"]
            ]
            self.assertEqual(points["points"][0]["state_delta"]["change_type"], "no_major_change")
            self.assertEqual(
                [point["reconstruction_sample_id"] for point in highlighted],
                ["000", "001"],
            )
            reconstruction = repository.reconstruction_index(
                Path(temporary_directory).name,
                2000,
            )
            self.assertEqual(len(reconstruction["samples"]), 2)

            vector_file = (
                Path(temporary_directory)
                / "synthesis"
                / "2000"
                / "transition_space"
                / "vectors.npz"
            )
            with np.load(vector_file) as vector_data:
                self.assertEqual(vector_data["mean_q"].shape, (5, 4))
                self.assertEqual(vector_data["z_sampled"].shape, (5, 4))
