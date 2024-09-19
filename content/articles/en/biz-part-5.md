# Road to 5 million: the programming (part 5)

Look, I ain't no coding genius. Everything I learned is from YouTube and [The Odin Project](http://theodinproject.com/) which are both free. And you can too, if you spend some time understanding how it all works.

TLDR: Coded up the minimum viable product.

![Get ready for nerd shit](/static/images/biz-series/peepo-nerd-glasses.gif)

## The front-end for N00bs

So you clicked this article and you see some text. How?

For a website to work, we need 4 things:

An HTML file, a computer for storing that file (server), an address to find that file, and a way to download and show that file to you (your browser). That's pretty much it.

You click a link, your browser sends a request to the server for a file, the server sends you the file, and your browser downloads it and shows it to you.

For example, this post that you are reading, it is an [HTML file](https://github.com/D-e-n-b-o-t/d-e-n-b-o-t.github.io/blob/main/articles/en/biz-series-part-5/index.html), which is stored on some computer controlled by Github, and has an address of [https://www.denislisunov.xyz](https://www.denislisunov.xyz) with a path to the file [/articles/en/biz-series-part-5/index.html](https://www.denislisunov.xyz/articles/en/biz-series-part-5/), which your browser downloaded and showed it to you.

The reason we call it HTML is because, in nerd speak, it stands for Hyper**Text** Markup Language. Its purpose is to display text. We use HTML code to display text.

So the first questions you might ask - how do you get colors in a text file?

Good question. 

The reason you see color, is because your browser knows how to read and display another type of code, used specifically for styling the text.

At first, nerds decided to store this beauty code on the same file as HTML, but later, other nerds decided to write beauty code into a separate file called CSS.

I included a link to my [CSS file](https://denislisunov.xyz/static/style.css) in this page, hidden from your eyes. And now, when you open this article, your browser not only downloads the HTML file, but also downloads the CSS file as well. So in reality, you just downloaded two files and your browser displayed them to you, both color and text!

Do you feel tricked reader? But wait, there's more!

Your browser has the ability to read not TWO but THREE types of code - text, style and scripts.

Before scripts, you would need to reload the page to update it. But reloading pages takes a long time, because it is heavy work for the server. 

So nerds decided, that the browser should be able to do some changes on its own. And that is how your browser gained the ability to download and read JavaScript (JS) files.

We, the web makers, use these scripts to manipulate what your browser does. 

With the power of scripts, your browser can download files, track information, send information, display different text, change the color and show you pesky pop-ups, all without reloading the page you are viewing. Isn't that scary?

You could be reading this post, and a script could be tracking your clicks, your scrolling activity, your reading time, recording your microphone, and sending that data somewhere. Ever heard of Google Analytics? This is basically how it works.

Or a script could be mining crypto with your browser and making $$$.

But I am a nice web maker. And this page you are on, only has two script files: To toggle the theme of this page, and to toggle sensitive mode. If there weren't any scripts, I, as the web maker, would have to have 4 different versions of this article. Imagine the headache!

<div class="filtered">

This message is avaible to you, because of a script.

</div>

So, full transparency, when you opened this page, your browser downloaded not two, but four files, because I included them within my HTML file! 

1 HTML, 1 CSS and 2 JS files.

All your browser can do is send, receive and display information.

I didn't mention this, because it is not important, but your browser can remember small bits of information. On this website, your browser remembers which theme you selected, and if you are using sensitive mode. If you clear your browsers cache, that information will be lost.

TLDR: Browser stronk.

## The back-end for N00bs

But you may wonder, how the fuck can I log into an account? How can I create a Gmail account? And how can I order my [Supreme brick](https://stockx.com/supreme-clay-brick-red) in an HTML file?

And the answer is that you can't. The front-end part is just visual feedback of what you receive from the server.

Whenever you open a link, you send a request to the server.

Remember I mentioned that you need a server aka. computer for storing your HTML file? Well, it has a bit more funcionality than just sending you files.

It is made out of 3 parts: the gateway, the pre-processor and the database.

The database is just that - a place to store data in. Your user accounts, passwords, etc.

The gateway is used to receive a request, redirect the request to a specific pre-processor and return a response. This is where your request initially lands.

The pre-processor is really just a function in any programming language that takes your request and generates a response.

Pre-processing requests raw (heh) isn't really recommended because it is hard to do it right. And this is why we use back-end frameworks. So every back-end framework is a pre-processor. All the logging in, creating users, and ordering a brick to your house, is done here.

The standard response from a pre-processor is an HTML template, which gets filled out with data from the pre-processing. So this is how you get a page that says you are logged in.

And then the gateway sends you that page, that was generated for you.

That's it. That is the standard webpage.

Ever heard REST API thrown around? It is a fancy way of saying that the response from the pre-processor will be in JSON format instead of HTML. And JSON is just specifically formatted data sent as text. 

It's way faster to send JSON data, because the pre-processor doesn't have to figure out, how to fill in an HTML template. And your browser can do that part, no problem.

## Back to biz

Created django project, split it into 4 parts for easier code management: `frontend`, `backend`, `database` and `api`.

For the `frontend`, I coded up some HTML templates for pages.

For the `backend`, I created views and forms that are needed.

For the `database`, I set up the ORM database for Users, Friend, Order and Dispute models.

The `api` folder is currently empty but I will create views and serializers there, if need be.

![Too simple? Time will tell.](/static/images/biz-series/profile-mvp.png)

The MVP version is done. It works. You can register, login, manage meetings, become a friend and update your profile. Payments have not been added, but will be added soon. Without payments, there is no way to make money. And we are making a business here.

Anyways, there are some things to left to add, which I will add over the upcoming months, to make the platform look more professional, and then onto marketing, getting feedback and improving.

Can't wait to release the project live.

Stay tuned.