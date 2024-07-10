from project import create_deck, create_groups, show_card_image
import pytest

def test_create_deck():
    assert len(create_deck()) ==  21 # Validate that 21 cards have been dealt.

def test_create_groups():
    assert len(create_groups(create_deck())) == 3 # Validate that 3 groups have been created

def test_show_card_image():
    assert show_card_image("img/2ofclubs.png") == None
    assert show_card_image("img/5ofhearts.png") == None
