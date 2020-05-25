# flashcardbot

## tasks

* [ ] Review flashcards, spaced repetition
* [ ] Send alert
* [ ] Do 'Done' step in each step?
* [ ] Connect to linguee for automatic context?

## heroku deployment

* <https://dashboard.heroku.com/apps/tflashcardbot>
* `heroku container:login`
* Make changes to project
* `heroku container:push web`
* `heroku container:release web`
* `heroku logs --tail`

## heroku resources

* [Simple bot in heroku](https://medium.com/python4you/creating-telegram-bot-and-deploying-it-on-heroku-471de1d96554)
* [Twitter bot in heroku, tests](https://dev.to/emcain/how-to-set-up-a-twitter-bot-with-python-and-heroku-1n39). [repo](https://github.com/emcain/drug_names)
* [Telegram bot on js, netlify and heroku](https://dev.to/jagedn/build-a-telegram-bot-using-netlify-47i1)

## enhancements

* [Flashcards to markdown table](https://core.telegram.org/bots/api#formatting-options)

## heroku tutorials for front-end

* `package.json`: name, version, engines, scripts, dependencies, keywords
* `Procfile`: web: node index.js. use the target that was previously defined to load the service

* <https://dashboard.heroku.com/apps/tflashcardbot/logs>
* [Where to host Telegram bots](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Where-to-host-Telegram-Bots)
* <https://devcenter.heroku.com/articles/how-heroku-works>

## resources

* [Supergroup manager bot with servers, sqlalchemy db](https://github.com/CubexX/confstat-bot)
* [Journey planner bot with docker, redis db, emojis](https://github.com/eigenein/ns-bot)
* [Prometheus alerting bot in Go](https://github.com/inCaller/prometheus_bot)
* [Bot that deletes messages with URL from users, mongodb, redis, bottle](https://github.com/lorien/daysandbox_bot)
* [Run a bot in google app engine](https://github.com/yukuku/telebot)
* [Imaginary friend bot, docker/redis, uses webhook in src/bot.py](https://github.com/telegram-bots/imaginaryfriend)
* [ankigenbot](https://github.com/damaru2/ankigenbot)
