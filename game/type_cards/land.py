from game.card import Card


class Land(Card):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.flag_dick:dict={}

    def generate_mana(self):
        pass

    def when_enter_battlefield(self):
        pass

    def when_leave_battlefield(self):
        pass

    def when_die(self):
        pass

    def when_sacrificed(self):#当牺牲时
        pass

    def when_clicked(self):#当地牌被电击时
        pass

    

