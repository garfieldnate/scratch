module ReadText (..) where

import Html exposing (Html, text, div, span)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import String exposing (slice, length)
import DynamicStyle exposing (hover)
import Signal exposing (Mailbox, Signal)

--Next: use a mailbox to display a word

type Action =
  ListWord Token | NoOp

type alias Token = {
  start : Int,
  end : Int
  }

type alias Model = {
  text : String,
  tokens : List(Token),
  display: List(Token)
}

initialModel : Model
initialModel = {
  text = "Hello my name is Nathan.",
  tokens = [
      {start = 0, end = 4},
      {start = 6, end = 7},
      {start = 9, end = 12},
      {start = 14, end = 15},
      {start = 17, end = 22}
    ],
    display = []
  }

update : Action -> Model -> Model
update action model =
    case action of
      NoOp -> model
      ListWord token -> { model | display = token::model.display}

actionMailbox : Mailbox Action
actionMailbox = Signal.mailbox NoOp

modelSignal : Signal Model
modelSignal =
  Signal.foldp update initialModel actionMailbox.signal

textStyle : List(Html.Attribute)
textStyle =
  (hover [("backgroundColor","white","#82caff")])
  --style
  --  [ ("backgroundColor", "#82caff")
  --  ]

textHtml : Signal.Address Action -> String -> Int -> List(Token) -> List(Html)
textHtml address modelText ind tokens =
  case tokens of
    hd::tl ->
    let
      tokenText = (slice hd.start (hd.end + 1) modelText)
      betweenText = (slice ind hd.start modelText)
    in
      [
        text betweenText,
        span ((textStyle)++[onClick address (ListWord hd)]) [
          text tokenText
          ]
         ] ++ (textHtml address modelText (hd.end + 1) tl)
    [] ->
      if ind < (length modelText)
      then [
        text (slice ind (length modelText) modelText)
        ]
      else []

listHtml address display =
  let writeSpan token =
    span [] [text (toString token.start)]
  in
    List.map writeSpan display

view : Signal.Address Action -> Model -> Html
view address model =
  div [
    style [("width", "100%"), ("overflow", "auto") ]
    ] [
      div [
        style [("float", "left"), ("width", "80%")]
      ] (textHtml address model.text 0 model.tokens),
      div [
        style [("float", "right"), ("border-left", "thick double")]
      ] (listHtml address model.display)
    ]
