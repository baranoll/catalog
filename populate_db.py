#!/usr/bin/python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_create import Genre, Base, Game, User

engine = create_engine('sqlite:///gameCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Dummy User", email="dummyUser@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Game for Action
genre = Genre(user_id=1, name="Action")

session.add(genre)
session.commit()

item = Game(user_id=1, name="Middle-earth: Shadow of War",
            description="Experience an epic open-world brought to life by the award-winning Nemesis System. Forge a new Ring of Power, conquer Fortresses in massive battles and dominate Mordor with your personal orc army in Middle-earth: Shadow of War.",
            developer="WB Games", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="MONSTER HUNTER: WORLD",
            description="Welcome to a new world! In Monster Hunter: World, the latest installment in the series, you can enjoy the ultimate hunting experience, using everything at your disposal to hunt monsters in a new world teeming with surprises and excitement. ",
            developer="CAPCOM Co., Ltd.", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Shadow of the Tomb Raider",
            description="As Lara Croft races to save the world from a Maya apocalypse, she must become the Tomb Raider she is destined to be. ",
            developer="Square Enix", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Assassin's Creed Odyssey",
            description="Choose your fate in Assassin's Creed Odyssey. From outcast to living legend, embark on an odyssey to uncover the secrets of your past and change the fate of Ancient Greece.",
            developer="Ubisoft", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Grand Theft Auto V",
            description="Los Santos is a city of bright lights, long nights and dirty secrets, and they don't come brighter, longer or dirtier than in GTA Online: After Hours. The party starts now.",
            developer="Rockstar North", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Tom Clancy's Ghost Recon Wildlands",
            description="Create a team with up to 3 friends in Tom Clancy's Ghost Recon Wildlands and enjoy the ultimate military shooter experience set in a massive, dangerous, and responsive open world. ",
            developer="Ubisoft", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="DOOM",
            description="Now includes all three premium DLC packs (Unto the Evil, Hell Followed, and Bloodfall), maps, modes, and weapons, as well as all feature updates including Arcade Mode, Photo Mode, and the latest Update 6.66, which brings further multiplayer improvements as well as revamps multiplayer progression. ",
            developer="Bethesda Softworks", genre=genre)

session.add(item)
session.commit()


# Game for Indie
genre = Genre(user_id=1, name="Indie")

session.add(genre)
session.commit()

item = Game(user_id=1, name="Stardew Valley",
            description="You've inherited your grandfather's old farm plot in Stardew Valley. Armed with hand-me-down tools and a few coins, you set out to begin your new life. Can you learn to live off the land and turn these overgrown fields into a thriving home? ",
            developer="ConcernedApe", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="FTL: Faster Than Light",
            description="This ""spaceship simulation roguelike-like"" allows you to take your ship and crew on an adventure through a randomly generated galaxy filled with glory and bitter defeat. ",
            developer="Subset Games", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Heat Signature",
            description="Heat Signature is a game from the developers of Gunpoint where you break into spaceships, make terrible mistakes, and think of clever ways out of them. You take a mission, fly to the target ship, sneak inside, and make clever use of your gadgets to distract, ambush and take out the crew. ",
            developer="Suspicious Developments", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Terraria",
            description="Dig, fight, explore, build! Nothing is impossible in this action-packed adventure game. Four Pack also available! ",
            developer="Re-Logic", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Don't Starve Together",
            description="Don't Starve Together is the standalone multiplayer expansion of the uncompromising survival game Don't Starve. ",
            developer="Klei Entertainment", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Oxygen Not Included",
            description="Oxygen Not Included is a space-colony simulation game. Deep inside an alien space rock your industrious crew will need to master science, overcome strange new lifeforms, and harness incredible space tech to survive, and possibly, thrive. ",
            developer="Klei Entertainment", genre=genre)

session.add(item)
session.commit()


# Game for Racing
genre = Genre(user_id=1, name="Racing")

session.add(genre)
session.commit()

item = Game(user_id=1, name="Dirt 4",
            description="DiRT 4 is all about embracing fear. It's about the thrill, exhilaration and adrenaline that is absolutely vital to off-road racing. It's about loving the feeling of pushing flat out next to a sheer cliff drop, going for the gap that's too small and seeing how much air you can get. Be Fearlessself. ",
            developer="Codemasters", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Project CARS 2",
            description="THE ULTIMATE DRIVER JOURNEY! Project CARS 2 delivers the soul of motor racing in the world's most beautiful, authentic, and technically-advanced racing game. ",
            developer="Slightly Mad Studios", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="The Crew 2",
            description="Take on the American motorsports scene as you explore and dominate the land, air, and sea across the entire USA. With a wide variety of cars, bikes, boats, and planes, compete in a wide range of driving disciplines. ",
            developer="Ubisoft", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Need For Speed: Hot Pursuit",
            description="Become Seacrest County's top cop or most wanted racer! ",
            developer="Criterion Games", genre=genre)

session.add(item)
session.commit()


# Game for Strategy
genre = Genre(user_id=1, name="Strategy")

session.add(genre)
session.commit()


item = Game(user_id=1, name="Total War: WARHAMMER II",
            description="Strategy gaming perfected. A breath-taking campaign of exploration, expansion and conquest across a fantasy world. Turn-based civilisation management and real-time epic strategy battles with thousands of troops and monsters at your command. ",
            developer="SEGA", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Sid Meier's Civilization VI",
            description="Civilization VI offers new ways to interact with your world, expand your empire across the map, advance your culture, and compete against history's greatest leaders to build a civilization that will stand the test of time. Play as one of 20 historical leaders including Roosevelt (America) and Victoria (England).",
            developer=" Firaxis Games, Aspyr (Mac), Aspyr (Linux)", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Frostpunk",
            description="Frostpunk is the first society survival game. As the ruler of the last city on Earth, it is your duty to manage both its citizens and its infrastructure. What decisions will you make to ensure your society's survival? What will you do when pushed to breaking point? Who will you become in the process? ",
            developer="11 bit studios", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="Stellaris",
            description="Explore a vast galaxy full of wonder! Paradox Development Studio, makers of the Crusader Kings and Europa Universalis series presents Stellaris, an evolution of the grand strategy genre with space exploration at its core. ",
            developer="Paradox Development Studio", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="XCOM 2",
            description="XCOM 2 is the sequel to the award-winning strategy game, XCOM: Enemy Unknown. Twenty years have passed since humanity lost the war against the alien invaders and a new world order now exists on Earth. After years of lurking in the shadows, XCOM forces must rise and eliminate the alien occupation. ",
            developer=" Firaxis Games, Feral Interactive (Mac), Feral Interactive (Linux)	", genre=genre)

session.add(item)
session.commit()

item = Game(user_id=1, name="BATTLETECH",
            description="Take command of your own mercenary outfit of 'Mechs and the MechWarriors that pilot them, struggling to stay afloat as you find yourself drawn into a brutal interstellar civil war. ",
            developer="Harebrained Schemes", genre=genre)

session.add(item)
session.commit()


print "added menu items!"
