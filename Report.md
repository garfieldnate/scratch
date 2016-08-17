# Project 2 Report: Portfolio Page

I know the rules are not to look at their example source, but I had to refer to it for some things. How did they do this or that? Just a quick peek for a hint and I'll figure out the rest for myself. FreeCodeCamp did NOT prepare me for this project. Tons of Googling did. I guess the community would have been a great help, but still it was a big surprise.

Things I learned from this project:

* Lots of Bootstrap, CSS and HTML
* Media queries for responsive pages
* Jade and SCSS. Sass watched my css directory and processed automatically, but Jade had to be run by hand after every save.
* Basic setup with SublimeText

Things I still need to learn:

* How to set up a full dev environment like code-pen but locally, with auto-preprocessing (Jade/Sass/CoffeeScript, etc.) and auto-reload.
* How to develop with Bootstrap source code (using the Sass mixins and variables)
* How to customize Bootstrap (but there is an online tool for this)

## Code Walkthrough

Two files: index.jade and style.scss. The Sassy CSS file can be compiled automatically into CSS in the background with `sass --watch css/`. The Jade file (or should I say Pug?) needed to be compiled each time with `pug index.jade`. Jade is a super simple replacement for HTML (although whitespace at the end of lines was slightly problematic with an editor that deletes those!). Sassy CSS is a superset of CSS that adds variables, mixins, nesting, and math, among other things. SASS files have a different syntax, so you have to make sure that the file extension matches the syntax you choose to use. 

I found several problems with my usage of Bootstrap using [Bootlint](https://github.com/twbs/bootlint).

###The Jade File

Start off the Jade file with the HTML5 doctype and some meta stuff that Bootstrap recommends/requires. Next, we include Bootstrap CSS and JS, jQuery, FontAwesome, and our custom CSS file.

The attributes on the `body` tag are for the BS "scrollspy" plugin, which highlights our navigation links as we scroll through the document. `#about-anchor` is for the navigation link, which I want to go as far to the top as possible. I could have just linked to `#` and it would have been the top of the page, too.

Next, we use a Bootstrap `.container`, which allows us to have a light gray space in the middle and a dark gray space on the outside (at certain page sizes). If we had used `.container-fluid`, the light gray would have filled the whole page.

Next was the navigation bar. With Bootstrap the navigation bar was complicated enough that it was honestly better to copy and paste working examples than to try and write it out yourself (I think I wrote and replaced at least 2 times). Some gotchas for me: 

* The first child of the nav-bar must be a BS `.container`/`.container-fluid`
* Leaving out the `div.navbar-header` results in not-great-looking formatting
* The anchor tags aren't allowed to be given `.nav-btn` or `.btn` due to BS3 limitations. Instead, you set the `ul` container to `.nav-pills`.
* All of the toggle/collapsey stuff is rather complicated.
* `.navbar-nav` is special, while `nav-default` is just styling.

Notice that `#nav-contents` is what I pointed the scrollspy plugin at in the `body` tag. It contains the special `.navbar-nav`, which has its `ul li a` styled and some of it's `ul li` set to `.active` (via scrollspy JS), which is then styled via other `ul .active a` rules.

I thought it was kind of interesting, by the way, that `span.icon-bar` adds a line to the "hamburger menu". 

The `main` tag holds the main content of a page, and as far as I can tell is good semantic HTML but does no styling. Same with `header` and `section`. The `header` and `section` tags consist of the main gray rectangles going down the center of the screen. In order to make them connect seamlessly, you have to add the `.clearfix` class, which makes them big enough to completely contain their children. Without that, the invisible margins of the contained `p` tags, etc. overflow the bottom, but the next section doesn't start until the end of that overflow. This causes an annoying gap. See [here](http://stackoverflow.com/a/29562362/474819).

The `hr` tags are highly stylized and contain a FontAwesome icon ("fa-code"); I'll explain when going through the CSS file.

The way Bootstrap's grid system CSS works is that there are 12 columns and you specify how many a given item takes up. You specify it for a specific size of device, and it applies to that size and higher. I decided to use lg, or 1024px, for the threshold of putting things side-by-side. 

So in the about section I use col-lg-8 to mean, "on large and up screens this will take 2/3rds of the available space." The image takes the other 1/3rd.

The formatting of the pictures in the portfolio section is a little complicated. When the screen is small the pictures appear as a single, centered column, and when it's big they appear as rows of two. To get proper spacing on both sides of and between these rows, we make a centered row 10 wide, and then within that make another row with each picture taking 6 columns (or half the available space). I've added special `left-col` and `right-col` classes to align the pictures on the left and right and leave space in the middle (the pictures' maximum width CSS makes sure there's space left between them). The images are also given the `img-responsive` class so that they resize automatically when we go to a lower screen size.

In the contact section, I have a form and a message side by side on a large screen and one after the other on a small screen. I put the message first in the HTML, but I use BS's push/pull to put it on the right when the screen is large. I had to do a custom move in the CSS of the little "no soliciting" note to get it to appear by the "submit" button at the bottom. I wanted a neat way of sticking it to the bottom but never found a good way. The form HTML is pretty normal, though it's highly stylized. Notice that I have label tags but there are no labels displayed; the labels are still important for accessibility, I believe.

The footer is divided into upper and lower so we can have a simple message and also a copyright. The little symbols are again FontAwesome. 

The social buttons sort of sucked to figure out the styling for. All of the classes except `.btn-circle` are from BS, and `btn-lg` was also customized for this.

Whew. I'll explain most of the styling in SCSS file section. But one thing bugs me: I was able to explain some of the formatting via the HTML markup. Is HTML/CSS really achieving a separation of content and formatting? In order to use BS you have to add tons of extra tags and lots and lots of classes. I mean, it's better than plain CSS, I suppose. But I don't think we've achieved the separation that is supposed to be the goal, here. If I wanted to change the look and feel of my page, I'd have to edit the HTML extensively.

## SCSS

At the top, I define lots of colors and a few sizes I plan to use.

The `container` mixin is used for `header` and `section`. It sets a maximum width and auto margins so that it is centered and you can see the background color of the body on the sides. The box-shadow makes it pop. I added box-shadows everywhere for poppiness.

The `body` is given a background color and some padding to make up for the space that gets blocked by the navigation bar (BS requires you to fix this yourself).

`.anchor`'s are what the navigator uses to link you to different parts of the page. There's a nasty problem where the anchor gets hidden by the navigation bar, and this is not mentioned in the BS docs. To fix it, you set the anchor to be an invisible block placed a ways down from its normal position.

The trick for making circles is to start with a square and then set the border radius to 50%.

The special hr's are made by giving them a thick, colored border and adding an :after containing a FontAwesome "code" icon. Where the icon goes is determined by the hr's text-center property. We limit the width to 512px on a big screen and 85% on a little screen. 

Next come the portfolio styles. The left and right columns are given text alignment on a big screen, and the images are made to auto-resize on a little screen. The inline-block and the HTML's `.text-center` class make them center nicely. Images are always given a margin so they don't fill a whole line.

The contact form was surprisingly straightforward: just code it to look like it is. Note, though, the `focus:` attributes which prevent a blue border from appearing when we select an entry to type in. Looking at this now, it could use some resizing/centering on medium and below devices. 

The next part that was difficult to figure out was the placement of the social icons within the circle buttons. They always appeared a little to low and to the left, which looks awful in a circle. I had to get the `i` tag to exactly overlap the containing `a` tag. To do this, I set the `a` position to relative, which does not move the `a` tag but allows specifying `absolute` in the child. Then we set the size to be the same as the parent (100% for `height` and `width`) and set the location to be the same as the parent (0 for `top` and `right`). We inherit the button's same padding, and therefore become the same size. Voila! Probably would have had to do the same thing for margin if the buttons had had any.

The last section is very kludgey. There's an online tool for customizing the colors in Bootstrap, but instead I just overrode them manually. Very gross, and not recommended. Notice that BS uses a 1px border along with shadow to really give a nice pop (again, with the corn). The orange colors were chosen by Googling "dark orange HTML" and then picking some other shades at http://www.color-hex.com/. And yes, orange was for Garfield.


