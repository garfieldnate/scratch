* Pattern matching exhaustiveness is not checked at compile-time. That seems bonkers, for a language with such a strong type system. I think we can do something about turning on warnings for this and then turning all warnings into errors.

* /= means "not equal"; I thought it meant "divided by equals" from reading it naively!

* From Simon Peyton-Jones:

> I’d like a better module system. Specifically, I want to be able to ship a Haskell package P to someone else, saying “P needs to import interfaces I and J from somewhere: you provide them, and it will offer interface K.” Haskell has no formal way to say this.

That's quite a drawback! No collections interfaces, then?
