use std::fmt;
use strum::IntoEnumIterator;
use strum_macros::EnumIter;
use rand::thread_rng;
use rand::seq::SliceRandom;

pub struct State {
    pub id: i32,
    pub players: (Player, Player),
    pub deck: Deck,
}

pub struct Player {
    pub id: i32,
    pub turn: bool,
    pub hand: Vec<Card>,
}

pub struct Deck {
    cards: Vec<Card>,
}

pub struct Card {
    pub suit: CardSuit,
    pub value: CardValue,
}

#[derive(EnumIter)]
pub enum CardSuit {
    Clubs,
    Diamonds,
    Hearts,
    Spades,
}

#[derive(EnumIter)]
pub enum CardValue {
    One,
    Two,
    Three,
    Four,
    Five,
    Six,
    Seven,
    Eight,
    Nine,
    Ten,
    Jack,
    Queen,
    King,
    Ace,
}

impl State {
    pub fn new(id: i32) -> Self {
        let deck = Deck::new();

        let players = (Player::new(1, deck.deal_hand()), Player::new(2, deck.deal_hand()));

        Self { id, players, deck }
    }
}

impl Player {
    pub fn new(id: i32, hand: Vec<Card>) -> Self {
        let turn = id == 0;
        
        Self { id, turn, hand }
    }
}

impl Deck {
    pub fn new() -> Self {
        let mut cards = Vec::new();
        for suit in CardSuit::iter() {
            for value in CardValue::iter() {
                cards.push(Card::new(suit, value));
            }
        }

        cards.shuffle(&mut thread_rng());

        Self { cards }
    }

    pub fn deal_hand(&self) -> Vec<Card> {
        let hand = Vec::new();
        for 0..7 { // a hand is seven cards
            hand.push(self.cards.pop());
        }

        hand
    }

    pub fn deal_card(&self) -> Card {
        self.cards.pop()
    }
}


impl fmt::Display for CardSuit {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            CardSuit::Clubs => write!(f, "Clubs"),
            CardSuit::Diamonds => write!(f, "Diamonds"),
            CardSuit::Hearts => write!(f, "Hearts"),
            CardSuit::Spades => write!(f, "Spades"),
        }
    }
}

impl CardValue {
    pub fn face_value(&self) -> i32 { // TODO might do this in a different way
        match self {
            CardValue::One => 1,
            CardValue::Two => 2,
            CardValue::Three => 3,
            CardValue::Four => 4,
            CardValue::Five => 5,
            CardValue::Six => 6,
            CardValue::Seven => 7,
            CardValue::Eight => 8,
            CardValue::Nine => 9,
            CardValue::Ten => 10,
            CardValue::Jack => 11,
            CardValue::Queen => 12,
            CardValue::King => 13,
            CardValue::Ace => 14,
        }
    }
}

impl fmt::Display for CardValue {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            CardValue::One => write!(f,"One"),
            CardValue::Two => write!(f, "Two"),
            CardValue::Three => write!(f, "Three"),
            CardValue::Four => write!(f, "Four"),
            CardValue::Five => write!(f, "Five"),
            CardValue::Six => write!(f, "Six"),
            CardValue::Seven => write!(f, "Seven"),
            CardValue::Eight => write!(f, "Eight"),
            CardValue::Nine => write!(f, "Nine"),
            CardValue::Ten => write!(f, "Ten"),
            CardValue::Jack => write!(f, "Jack"),
            CardValue::Queen => write!(f, "Queen"),
            CardValue::King => write!(f, "King"),
            CardValue::Ace => write!(f, "Ace"),
        }
    }
}
