# -*- coding: utf-8 -*-
import numpy
import utils
import simulator
import random
import strategy
import pandas
from datetime import datetime
from dateutil.relativedelta import relativedelta
from strategy import CombinationCreator
from loader import Loader
from simulator import Appliable

# どの戦略をアンサンブルするかはここのimportで指定する
from strategies.production.combination import CombinationStrategy

class CombinationStrategy(CombinationStrategy):
    def __init__(self, setting):
        self.files = setting.ensemble
        self.strategies = strategy.create_ensemble_strategies(self.files)
        super().__init__(setting)

    def common(self, setting):
        return self.default_common()

    def get_size(self, size):
        return size if size < self.setting.condition_size else self.setting.condition_size

    def rules(self, rule):
        return [
            lambda x: rule.apply(x),
            lambda x: not rule.apply(x)
        ]

    def conditions_by_seed(self, seed):

        new_rules         = sum(list(map(lambda x: self.rules(x.new_rules[0]), self.strategies)), [])
        taking_rules      = sum(list(map(lambda x: self.rules(x.taking_rules[0]), self.strategies)), [])
        stop_loss_rules   = sum(list(map(lambda x: self.rules(x.stop_loss_rules[0]), self.strategies)), [])
        closing_rules     = sum(list(map(lambda x: self.rules(x.closing_rules[0]), self.strategies)), [])
        x2_rules          = sum(list(map(lambda x: self.rules(x.x2_rules[0]), self.strategies)), [])
        x4_rules          = sum(list(map(lambda x: self.rules(x.x4_rules[0]), self.strategies)), [])
        x8_rules          = sum(list(map(lambda x: self.rules(x.x8_rules[0]), self.strategies)), [])

        new_rules = new_rules + taking_rules + stop_loss_rules

        random.seed(seed)
        numpy.random.seed(seed)

        size = self.get_size(len(self.strategies))

        new, self.new_conditions                = self.choice(new_rules, size*2, self.apply_weights("new", len(new_rules)))
        taking, self.taking_conditions          = self.choice(taking_rules, size, self.apply_weights("taking", len(taking_rules)))
        stop_loss, self.stop_loss_conditions    = self.choice(stop_loss_rules, size, self.apply_weights("stop_loss", len(stop_loss_rules)))
        closing, self.closing_conditions        = self.choice(closing_rules, size, self.apply_weights("closing", len(closing_rules)))
        x2, self.x2_conditions                  = self.choice(x2_rules, size, self.apply_weights("x2", len(x2_rules)))
        x4, self.x4_conditions                  = self.choice(x4_rules, size, self.apply_weights("x4", len(x4_rules)))
        x8, self.x8_conditions                  = self.choice(x8_rules, size, self.apply_weights("x8", len(x8_rules)))

        # 選択された条件のインデックスを覚えておく
        self.selected_condition_index = {
            "new":new, "taking": taking, "stop_loss": stop_loss, "closing": closing, "x2": x2, "x4": x4, "x8": x8
        }

