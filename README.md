# flashcardbot

## tasks

* [ ] Make bot more presentable
* [ ] demo of bot behavior in readme
* [ ] Add handlers for start, Done
* [~] Data isn't persistent in heroku
  * <https://cloud.mongodb.com/>
  * <https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent>
  * <https://github.com/David-Lor/Telegram-BusBot-DataManager>
  * <https://medium.com/@voronov007/telegram-bot-from-scratch-development-with-python-and-deploying-on-free-of-costs-server-from-2463f2b63d83>
  * <https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb>
* [ ] Review flashcards, spaced repetition
* [ ] Send alert
* [ ] Do 'Done' step in each step? @mongodb
* [ ] Connect to linguee for automatic context?

## mongodb

```python
user_id = update.message.from_user.id
user_collection = db.user_id # is the user's json/dict
# make sure user collection has a text index
user_collection.create_index([('post', TEXT)], default_language='english')
last_added = user_collection.find({}).sort('_id', -1).next()

def stats(bot, update):
    user = update.message.from_user
    user_coll = get_user_collection(user)
    response = '🗄 Your Daytobase has {} records\n'.format(user_coll.count())

    if user.id in settings.ADMIN_IDS:
        client = MongoClient()
        db = client['daytobase']
        coll_counts = [db[coll].count() for coll in db.collection_names()]
        response += '\nDaytobase has `{}` users\n'.format(len(coll_counts))
        response += 'Biggest collection sizes: `{}`\n'.format(sorted(coll_counts)[-3:])

        month_ago = datetime.utcnow() - timedelta(days=30)
        recent_counts = [db[coll].find({'time': {'$gt': month_ago}}).count()
                         for coll in db.collection_names()]
        response += 'New records over past 30 days:  `{}`\n'.format(sum(recent_counts))
        active_colls = sum([c > 0 for c in recent_counts])
        response += 'Users active over past 30 days: `{}`\n'.format(active_colls)

    update.message.reply_text(response, parse_mode='Markdown')

# from https://github.com/lorien/daysandbox_bot
def connect_db():
    db = MongoClient()['daysandbox']
    db.user.create_index('username', unique=True)
    db.joined_user.create_index([('chat_id', 1), ('user_id', 1)])
    db.event.create_index([('type', 1), ('date', 1)])
    db.day_stat.create_index('date')
    return db
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
