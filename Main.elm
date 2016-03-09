import ReadText
import Html exposing (Html, text, div, span)
import Signal exposing (Mailbox, Signal)

type Action =
  ReadTextAction ReadText.Action | NoOp

type alias Model = {
  readTextModel: ReadText.Model
}

initialModel : Model
initialModel = {
  readTextModel = ReadText.initialModel
  }

update : Action -> Model -> Model
update action model =
    case action of
      NoOp -> model
      ReadTextAction action  -> { model | readTextModel = ReadText.update action model.readTextModel}

actionMailbox : Mailbox Action
actionMailbox = Signal.mailbox NoOp

modelSignal : Signal Model
modelSignal =
  Signal.foldp update initialModel actionMailbox.signal

view : Signal.Address Action -> Model -> Html
view address model =
  div [] [
    ReadText.view (Signal.forwardTo address ReadTextAction) model.readTextModel
  ]

main : Signal Html
main =
  Signal.map (view actionMailbox.address) modelSignal

