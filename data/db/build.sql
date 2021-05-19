CREATE TABLE IF NOT EXISTS guilds (
        GuildID integer PRIMARY KEY,
        Prefix text DEFAULT "poo.",
        ghostID integer,
        introChannel integer

);

CREATE TABLE IF NOT EXISTS modusage (
        daysSinceFunny integer,
        dateOfFunny date

);

CREATE TABLE IF NOT EXISTS users (
        UserID integer PRIMARY KEY,
        XP integer DEFAULT 0,
        lvl integer DEFAULT 0,
        XPLock text DEFAULT CURRENT_TIMESTAMP,
        birthday date,
        LevelChannel integer 
);