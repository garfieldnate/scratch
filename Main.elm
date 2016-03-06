import Html exposing (text, div, span)
import Html.Attributes exposing (style)
import String exposing (slice, length)
--identicalSnowflake
import DynamicStyle exposing (hover)
import List

type alias Token = {
  start : Int,
  end : Int
  }


model = {
  text = "hello my name is Nathan",
  tokens = [{start = 0, end=4}, {start = 6, end=7}, {start=9, end=12}, {start=14, end=15}, {start=17, end=23}]
  }

highlightStyle =
  (hover [("backgroundColor","white","#82caff")])
  --style
  --  [ ("backgroundColor", "#82caff")
  --  ]

highlight : String -> Int -> List(Token) -> List(Html.Html)
highlight modelText ind tokens =
  case tokens of
    hd::tl ->
    let
      tokenText = (slice hd.start (hd.end + 1) modelText)
      betweenText = (slice ind hd.start modelText)
    in
      [
        text betweenText,
        span highlightStyle [
          text tokenText
          ]
         ] ++ (highlight modelText (hd.end + 1) tl)
    [] ->
      if ind < (length modelText)
      then [
        text (slice ind (length modelText) modelText)
        ]
      else []

main =
  div []
    (highlight model.text 0 model.tokens)

