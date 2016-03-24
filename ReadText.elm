--Next: gracefully handle Json and Http errors
module ReadText (..) where

import StartApp
import Html exposing (Html, text, div, body, span, button)
import Html.Attributes exposing (style, class)
import Html.Events exposing (onClick)
import String exposing (slice, length)
import DynamicStyle exposing (hover)
import Signal exposing (Mailbox, Signal)
import Http
import Task exposing (Task, andThen)
import Effects exposing (Effects)
import Json.Decode as Json exposing ((:=))
import Dict exposing (Dict)

--Next: use a mailbox to display a word

type Action =
  ListWord Vocab
  | Refresh
  | NewText (Maybe Model)
  | NoOp

type alias Token = {
    start : Int
  , end : Int
  , lemma : String
  , details : Dict String String
  }

type alias Vocab = {
    lemma : String
  , example : String
  , definition : String
  , tags: Dict String String
}

type alias Model = {
  text : String,
  tokens : List(Token),
  vocab : List(Vocab)
}

init : (Model, Effects Action)
init = ({
  text = "",
  tokens = [],
    vocab = []
  }, Effects.none)

update : Action -> Model -> (Model, Effects Action)
update action model =
    case action of
      NoOp -> (model, Effects.none)
      ListWord v -> (
        { model | vocab = v::model.vocab}, Effects.none)
      NewText fetchedModel ->
        case fetchedModel of
          Just fm -> (fm, Effects.none)
          Nothing -> ({text = "nothing retrieved", tokens = [], vocab = []}, Effects.none)
      Refresh -> (model, refreshFx)

textUrl = "http://localhost:3000/en"

refreshFx :Effects Action
refreshFx =
  Http.get decodeText textUrl
    |> Task.toMaybe
    |> Task.map NewText
    |> Effects.task

--actionMailbox : Mailbox Action
--actionMailbox = Signal.mailbox NoOp

--modelSignal : Signal (Model, Effects Action)
--modelSignal =
--  Signal.foldp update init actionMailbox.signal

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
        span ((textStyle)++[onClick address (ListWord (token2vocab hd))]) [
          text tokenText
          ]
         ] ++ (textHtml address modelText (hd.end + 1) tl)
    [] ->
      if ind < (length modelText)
      then [
        text (slice ind (length modelText) modelText)
        ]
      else []

token2vocab: Token -> Vocab
token2vocab token = {
    lemma = token.lemma
  , tags = token.details
  , example = "" --TODO
  , definition = "" --TODO
  }

listHtml : Signal.Address Action -> List(Vocab) -> Html
listHtml address vocab =
  let writeSpan v =
    div [] [
      div [class "item"] [
        text v.lemma
      ]
      , div [class "ui special popup"] [
          div [class "header"] [text v.lemma]
        , div [] [text v.definition]
      ]
    ]
  in
    div [
        class "ui celled list"
    ] (List.map writeSpan vocab)

view : Signal.Address Action -> Model -> Html
view address model =
  div [
        class "ui bottom attached segment"
      ] [
      div [] (List.concat [
        (textHtml address model.text 0 model.tokens),
          [
            button [
            onClick address Refresh, class "ui button"
            ] [ text "Refresh" ]
          ]
        ])
     , (listHtml address model.vocab)
  ]

decodeText : Json.Decoder Model
decodeText =
  let token =
        Json.object4 Token
          ("start" := Json.int)
          ("end" := Json.int)
          ("lemma" := Json.string)
          ("details" := Json.dict Json.string)
      vocab =
        Json.object4 Vocab
          ("lemma" := Json.string)
          ("example" := Json.string)
          ("definition" := Json.string)
          ("tags" := Json.dict Json.string)
  in
    Json.object3 Model
      ("text" := Json.string)
      ("tokens" := Json.list token)
      ("vocab" := Json.list vocab)
