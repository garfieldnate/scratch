module ReadText (..) where

import Html exposing (Html, text, div, span)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import String exposing (slice, length)
import DynamicStyle exposing (hover)
import Signal exposing (Mailbox, Signal)
import Http
import Task exposing (Task, andThen)
import Effects exposing (Effects)
import Json.Decode exposing (decodeValue, Decoder)

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

init : (Model, Effects Action)
init = ({
  text = "",
  tokens = [],
    display = []
  }, Effects.none)

update : Action -> Model -> (Model, Effects Action)
update action model =
    case action of
      NoOp -> (model, Effects.none)
      ListWord token -> ({ model | display = token::model.display}, Effects.none)
      NewText fetchedModel -> ({
        text = fetchedModel.text,
        tokens = fetchedModel.tokens,
        display = []
      }, Effects.none)

actionMailbox : Mailbox Action
actionMailbox = Signal.mailbox NoOp

--Next: update as shown in http://www.elm-tutorial.org/040_effects/effects_2.html
modelSignal : Signal (Model, Effects Action)
modelSignal =
  Signal.foldp update init actionMailbox.signal

textStyle : List(Html.Attribute)
textStyle =
  (hover [("backgroundColor","white","#82caff")])

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

textUrl = "http://localhost:3000/en"

requestText :Effects Action
requestText =
  Http.get decodeText textUrl
    |> Task.toMaybe
    |> Task.map NewText
    |> Effects.task

decodeText =
  decodeValue (Decoder Model)
    --object2 (,)
    --  ("text" := string)
    --  ("text" := List(Token))