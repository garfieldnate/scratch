import Html exposing (Html, text, div, span)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import String exposing (slice, length)
import DynamicStyle exposing (hover)
import Signal exposing (Mailbox, Signal)

--Next: use a mailbox to display a word

type Action =
  ListWord Token | Nothing

type alias Token = {
  start : Int,
  end : Int
  }

model = {
  text = "Hello my name is Nathan.",
  tokens = [
      {start = 0, end = 4},
      {start = 6, end = 7},
      {start = 9, end = 12},
      {start = 14, end = 15},
      {start = 17, end = 22}
    ]
  }

actionMailbox : Mailbox Action
actionMailbox = Signal.mailbox Nothing

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

textWindow : Signal.Address Action -> String -> List(Token) -> Html
-- Left 80% contains text, right 20% contains vocab last
textWindow address modelText tokens =
  div [
    style [("width", "100%"), ("overflow", "auto") ]
    ] [
      div [
        style [("float", "left"), ("width", "80%")]
      ] (textHtml address modelText 0 tokens),
      div [
        style [("float", "right"), ("border-left", "thick double")]
      ] [] --next: add list of vocab here, and add more when click on
    ]

update address action =
  textWindow address model.text model.tokens

main : Signal Html
main =
  Signal.map (update actionMailbox.address) actionMailbox.signal

