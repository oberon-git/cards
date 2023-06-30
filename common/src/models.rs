use std::fmt;

pub struct State {
    pub id: i32,
    pub players: (Player, Player),
    pub deck: Vec<Card>,
}

pub struct Player {
    pub id: i32,
    pub turn: bool,
    pub hand: Vec<Card>,
}

pub struct Card {
    pub suit: CardSuit,
    pub value: CardValue,
}

pub enum CardSuit {
    Clubs,
    Diamonds,
    Hearts,
    Spades,
}

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
