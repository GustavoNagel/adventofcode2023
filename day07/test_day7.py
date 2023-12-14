import pytest
from .main import Hand, HandType, run

test_inputs = (
    ("32T3K", HandType.ONE_PAIR, 765),
    ("T55J5", HandType.THREE_OF_A_KIND, 684),
    ("KK677", HandType.TWO_PAIR, 28),
    ("KTJJT", HandType.TWO_PAIR, 220),
    ("QQQJA", HandType.THREE_OF_A_KIND, 483),
)
@pytest.mark.parametrize("cards,expected_type,bid", test_inputs)
def test_almanac_map(cards: str, expected_type: HandType, bid: int):
    hand = Hand(cards, bid)
    hand.simple_score
    assert hand.main_type == expected_type

def test_rank():
    hands_list = [Hand(cards, bid) for cards, _, bid in test_inputs]
    sorted_hands = sorted(hands_list)
    assert [hand.cards for hand in sorted_hands] == ["32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"]
    assert [hand.bid for hand in sorted_hands] == [765, 220, 28, 684, 483]

test_inputs_joker = (
    ("32T3K", HandType.ONE_PAIR, 765),
    ("T55J5", HandType.FOUR_OF_A_KIND, 684),
    ("KK677", HandType.TWO_PAIR, 28),
    ("KTJJT", HandType.FOUR_OF_A_KIND, 220),
    ("QQQJA", HandType.FOUR_OF_A_KIND, 483),
)
@pytest.mark.parametrize("cards,expected_type,bid", test_inputs_joker)
def test_almanac_map_joker(cards: str, expected_type: HandType, bid: int):
    hand = Hand(cards, bid, joker_rule=True)
    hand.simple_score
    print(hand.cards, hand.cards_joker, hand.get_cards_without_jokers())
    assert hand.main_type == expected_type

def test_rank_joker():
    hands_list = [Hand(cards, bid, joker_rule=True) for cards, _, bid in test_inputs_joker]
    sorted_hands = sorted(hands_list)
    assert [hand.cards for hand in sorted_hands] == ["32T3K", "KK677", "T55J5", "QQQJA", "KTJJT"]
    assert [hand.bid for hand in sorted_hands] == [765, 28, 684, 483, 220]

def test_run():
    assert run(filename="day07/testing_file.txt") == 6440
    assert run(filename="day07/testing_file.txt", joker_rule=True) == 5905