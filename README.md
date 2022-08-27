# flashcardbot

## tasks

* [ ] Adapt review_flashcards to mongodb
* [ ] Make different decks for diff languages
* [ ] Get back to menu easier
* [ ] Add handlers for start, Done. Maybe even delete start
* [ ] demo of bot behavior in readme
* [ ] Review flashcards, spaced repetition
* [ ] Send alert
* [ ] Do 'Done' step in each step? @mongodb how does it end the session?
* [ ] Connect to linguee for automatic context?
* [ ] Check @ankigen_bot in telegram
* [ ] if = in text, add flashcard

## mongodb

* [MongoDB Atlas cloud](https://cloud.mongodb.com/)
* [To update collection](https://docs.mongodb.com/manual/reference/operator/update/set/)
* App was warking in local, not in heroku. Only the local IP was whitelisted in MongoDB, had to put [0.0.0.0/0](https://stackoverflow.com/a/42170205/4569908)
* [Mongodb python tutorial](http://zetcode.com/python/pymongo/): greater than, sort, aggregate, limit data output

## persistence

* [First used pickle persistence](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent)

```python
# Create the Updater and pass it your bot's token.
pp = PicklePersistence(filename='data.pkl')

updater = Updater(token, persistence=pp, use_context=True)

# in ConversationHandler, under fallbacks, name
persistent=True

# then use context.user_data as dict in handlers
context.user_data[new_word] = word_context
```

## heroku

### deployment

* <https://dashboard.heroku.com/apps/tflashcardbot>
* `heroku container:login`
* Make changes to project
* `heroku container:push web`
* `heroku container:release web`
* `heroku logs --tail`
* To stop the app: `heroku ps:scale web=0`. Manually scale to web=1 afterwards.

### heroku resources

* [Simple bot in heroku](https://medium.com/python4you/creating-telegram-bot-and-deploying-it-on-heroku-471de1d96554)
* [Twitter bot in heroku, tests](https://dev.to/emcain/how-to-set-up-a-twitter-bot-with-python-and-heroku-1n39). [repo](https://github.com/emcain/drug_names)
* [Telegram bot on js, netlify and heroku](https://dev.to/jagedn/build-a-telegram-bot-using-netlify-47i1)

### heroku tutorials for front-end

* `package.json`: name, version, engines, scripts, dependencies, keywords
* `Procfile`: web: node index.js. use the target that was previously defined to load the service

* <https://dashboard.heroku.com/apps/tflashcardbot/logs>
* [Where to host Telegram bots](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Where-to-host-Telegram-Bots)
* <https://devcenter.heroku.com/articles/how-heroku-works>

## docker & heroku

* Need a [heroku.yml](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml) file. If you don’t include a run section in the yml, Heroku uses the CMD specified in the Dockerfile.

## enhancements

* [Flashcards to markdown table](https://core.telegram.org/bots/api#formatting-options)

## resources

* [Supergroup manager bot with servers, sqlalchemy db](https://github.com/CubexX/confstat-bot)
* [Journey planner bot with docker, redis db, emojis](https://github.com/eigenein/ns-bot)
* [Prometheus alerting bot in Go](https://github.com/inCaller/prometheus_bot)
* [Bot that deletes messages with URL from users, mongodb, redis, bottle](https://github.com/lorien/daysandbox_bot)
* [Run a bot in google app engine](https://github.com/yukuku/telebot)
* [Imaginary friend bot, docker/redis, uses webhook in src/bot.py](https://github.com/telegram-bots/imaginaryfriend)
* [ankigenbot](https://github.com/damaru2/ankigenbot)
* [Apartments bot: facebook parsing, lowdb, js, tests](https://snir.dev/blog/apartments-bot/). [Github repo](https://github.com/snird/apartments_bot)
* [Persistent bot about a transportation service: rest api, mongodb](https://github.com/David-Lor/Telegram-BusBot-DataManager)
* [Bot on python, django, rest api, heroku](https://medium.com/@voronov007/telegram-bot-from-scratch-development-with-python-and-deploying-on-free-of-costs-server-from-2463f2b63d83)
* [Todoist bot, python](https://github.com/ihoru/todoist_bot)
