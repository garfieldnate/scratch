# Pharo notes

* brew cask is from April, but website latest release is from July. It's December right now, so I don't see why the cask isn't updated!
* Couldn't open on Mac without triggering security warning. Had to right-click and force Mac to open it.

    hn_mac_security_error.png
    https://news.ycombinator.com/item?id=22113924

* Clicked on an image, which opened a small window saying it was downloading stuff; I didn't want to do that, so I clicked the big red X. That did nothing. I clicked it a whole bunch and nothing happened, not even an animation showing the X being clicked. Eventually the HTTP request failed and a good 10 error windows popped up. Not a great experience.

    tons_of_errors.png

* First impression of UI: everything is small and difficult to read; one of the icons at the top has a name that gets cut off with ... because it's too long.

	first_impression_small.png

* Settings allow making the text bigger, but the main menu icons didn't get any bigger, so now the text is just cut off everywhere. Also, the main menu wouldn't resize until I changed the theme between light and dark. Changing the theme causes the settings menu to close immediately.

    larger_text_same_size_icons.png

* Really strange, buggy, annoying behavior when trying to scroll through a list. If the parent item is highlighted, then scrolling too far closes the list. If an aunt/uncle item is highlighted, then scrolling fails and the screen stutters as it tries to take you back to the highlighted item while you are trying to scroll down.
	
	buggy_scrolling.mov

* When I launched an image, Pharo started up with Dark Mode, while the image launcher had light mode. It probably got that from my computer settings, and the image launcher did not do the same. Also, the text is horribly thin and difficult to read.

    wrong_theme.png

* Help does not use the normal MacOS facilities, so I can't search for commands quickly. Why is this part hand-rolled, and why is there no search functionality?

* Enlarged the text size for Pharo; once again, it wouldn't update until the theme was changed (but the settings window doesn't automatically close, which is nice). Then the various UI elements didn't adjust, so the text was getting cut off. Plus, the main menu text stays the same tiny size.

    pharo_text_too_big.png

* Asks for author's name for signing a commit, but then says you can't spell your name correctly unless it's an ASCII subset. Should really call it a "handle" or something.

    ridiculous_name_constraints.png

* Pretty cool that it's got linting built in there! Kind of weird that there are already issues being found, though, as I'm just typing in text from the tutorial (https://github.com/pharo-open-documentation/pharo-wiki/blob/master/General/SettingUpANewProject.md).

    linting_tutorial.png

* Scrolling in a text window causes the cursor to move and select text. But it is *very* janky; moves forward and backward, is very slow, and also moves the window at the same time. Super weird!

* ESC should press the cancel button on an open window.

* Tutorial does not say how to run a unit test. Right clicked on MyCounterTest and could run the tests; I guess it's CMD+T. But the test passed, and the tutorial said it should fail!

* Can we not put "A test that will..." in our docstrings for methods that are already in test classes and are already named `testXYZ`?

* Pasted two tests into one file, and the text for the second test was mostly red; I guess that's not allowed? No error messages of any kind were provided.

* I like that the correct shortcut is shown in an overlay whenever I use a menu instead of the shortcut.

* The package browser disappeared and now I don't know how to get it back.

- Found it much later! Have to double-click on tab titles. Right clicking on them does nothing, though...

* When I press CMD+S from the text window, the window flashes, but when I go to close out I'm warned that I will lose changes that haven't been saved, and the warning window doesn't have any button to allow me to save. The menu tells me it's actually CMD+shift+S... okay, I've saved. But when I go to close, it tells me it hasn't been saved! Argh!

* Couldn't figure out how to create more tests. When I click on the test class and then on the 'tests' protocol I created, all I get is an `inst. side method` window. I put the increment and decrement tests in new windows with this name, but the window names aren't updating to anything and the list of tests isn't updated. Don't know how to add tests.

Okay, I have to ditch this tutorial. This is a disaster and I'm completely lost.

Now I'll go throught the MOOC instead. https://www.youtube.com/playlist?list=PL2okA_2qDJ-kCHVcNXdO5wsUZJCY31zwf

* [video 4] Am I correct to think that `new` and `new:` are two different message names? I really hope not. I hope that's just syntax. 
* Why is Point built-in like strings and numbers? It's either silly or intriguing.
* [video 5] It's confusing to me that the block takes a named argument `:value` instead of a unary argument. Took a bit of internetting to figure out that the REPL is called a Playground (why didn't the course start with this?). `[ :x|x*x+3 ] 2` does not work, but `[ :x|x*x+3 ] value:2` does not (`End of statement list encountered`). Not really sure why, but whatevs for now, I guess.
*  Okay, ProfStef is great!
* How do I quickly jump to the documentation for a class? Like, I'm at 17/29 in ProfStef and I just want to look at the documentation for Transcript. How do I do that?
* Using the "Basic Inspect" command gives a bunch of warning windows about something being deprecated.
* It's really strange to me that printing a value puts it right in the same window. I think it would be better somewhere else. This is bound to cause some silly errors.
* When I click on a scroll button for a window, it scrolls all the way to the bottom or top of the window instead of a single line.

    stuck_scroll_buttons.mov

* ProfStef 23 is giving me an error:

    #(11 38 3 -2 10) do: [:each |
     Transcript show: each printString; cr].

    #(11 38 3 -2 10) do: [:each |
     Transcript show: each printString; cr Unknown input at end ->].

 Hmm, it appears that it works fine if I remove the newline after `|`.

 Ah, the issue was that I had to select the whole line! The behavior I expected was that if I were at the end of a line it would understand that it should execute the whole line.

 Seriously, there should at least be a shortcut for highlighting the entire expression the cursor is sitting in.

 * 24: "Please use only Do it or Print it on this page, not Inspect it." -> would that cause some infinite recursion or something?

 * 24: I wanna know what `actionSelector: #value;` does for SimpleButtonMorph. 

 * 24: Clicking on that button didn't delete the button like it was supposed to. Running `SimpleButtonMorph allInstances last delete` doesn't delete it either. Is that because I decided to inspect the button creation code? Turned out that there were 21 of that button! I deleted them all with `SimpleButtonMorph allInstances do: [ :each | each delete ].`. That means I'm learning, right? :D \o/

 * In general, there just seem to be a ton of typos around in the core product.

 * That last lesson with the debugger was really exciting and finally I got to see why this is supposed to be great. Why is there only a tutorial on the synax?

 * 