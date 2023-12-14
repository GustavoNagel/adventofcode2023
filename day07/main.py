from functools import total_ordering
from itertools import groupby
from enum import IntEnum


class HandType(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

len_reference = {
    5: HandType.FIVE_OF_A_KIND,
    4: HandType.FOUR_OF_A_KIND,
    3: HandType.THREE_OF_A_KIND,
    2: HandType.ONE_PAIR,
    1: HandType.HIGH_CARD,
}

cards_order = "23456789TJQKA"
indices = {c: i + 1 for i, c in enumerate(cards_order)}

cards_order_joker = "J23456789TQKA"
indices_joker = {c: i + 1 for i, c in enumerate(cards_order_joker)}

@total_ordering
class Hand:

    cards_joker = None

    def __init__(self, cards: str, bid: str | int, joker_rule: bool = False) -> None:
        self.cards = cards
        self.bid = int(bid)
        self.joker_rule = joker_rule
        self.simple_points = [indices[k] if not joker_rule else indices_joker[k] for k in cards]
        self.cards_joker = self.get_cards_without_jokers()

    def __eq__(self, other: 'Hand'):
        return self.simple_score == other.simple_score

    def __lt__(self, other: 'Hand'):
        return self.simple_score < other.simple_score

    def get_sorted_groups(self):
        cards = self.cards_joker or self.cards
        ind = indices_joker if self.joker_rule else indices
        return sorted(
            [(len(list(g)), ind[k], k)for k, g in groupby(sorted(cards, key=ind.get))],
            key=lambda x: x[0] * 100 + x[1],
            reverse=True
        )

    def get_cards_without_jokers(self):
        if self.joker_rule and 'J' in self.cards:
            for _, _, k in self.get_sorted_groups():
                if k != 'J':
                    break
            return self.cards.replace('J', k)
        return self.cards

    @property
    def poker_score(self):
        """Poker Score point (not used).

        Five of a kind, where all five cards have the same label: AAAAA
        Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        High card, where all cards' labels are distinct: 23456
        """
        self.main_type = HandType.HIGH_CARD
        points = []
        for n, p, _ in self.get_sorted_groups():
            points.append(p)
            hand_type = len_reference.get(n)
            if hand_type >= HandType.ONE_PAIR:
                if self.main_type == HandType.THREE_OF_A_KIND:
                    hand_type = HandType.FULL_HOUSE
                elif self.main_type == HandType.ONE_PAIR:
                    hand_type = HandType.TWO_PAIR
                self.main_type = hand_type
        return [self.main_type] + points

    @property
    def simple_score(self):
        """Simple score point.

        Five of a kind, where all five cards have the same label: AAAAA
        Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        High card, where all cards' labels are distinct: 23456
        """
        self.main_type = HandType.HIGH_CARD
        for n, _, _ in self.get_sorted_groups():
            hand_type = len_reference.get(n)
            if hand_type >= HandType.ONE_PAIR:
                if self.main_type == HandType.THREE_OF_A_KIND:
                    hand_type = HandType.FULL_HOUSE
                elif self.main_type == HandType.ONE_PAIR:
                    hand_type = HandType.TWO_PAIR
                self.main_type = hand_type
        return [self.main_type] + self.simple_points

def run(filename: str, joker_rule: bool = False):
    with open(filename, 'r') as file:
        hands = [Hand(*line.split(), joker_rule=joker_rule) for line in file]
    for i, hand in enumerate(sorted(hands)):
        print(i, hand.cards, hand.cards_joker, hand.get_sorted_groups())
    return sum(hand.bid * (i + 1) for i, hand in enumerate(sorted(hands)))

if __name__ == "__main__":
    print(run("input_file.txt"))
    print(run("input_file.txt", True)) # 253680676 errado