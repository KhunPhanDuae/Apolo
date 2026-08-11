const Database = require("better-sqlite3");

const db = new Database("database.db");

// Table တည်ဆောက်ခြင်း
db.exec(`
    CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY,
        draft_title TEXT NOT NULL,
        draft_description TEXT NOT NULL,

        production_title TEXT NOT NULL,
        production_description TEXT NOT NULL,

        status TEXT NOT NULL DEFAULT 'draft',
        tested INTEGER NOT NULL DEFAULT 0,

        updated_at TEXT NOT NULL
    )
`);

// ပထမဆုံး run တဲ့အချိန် data ထည့်မယ်
const existing = db
    .prepare("SELECT id FROM pages WHERE id = 1")
    .get();

if (!existing) {

    db.prepare(`
        INSERT INTO pages (
            id,
            draft_title,
            draft_description,
            production_title,
            production_description,
            status,
            tested,
            updated_at
        )
        VALUES (
            1,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
    `).run(
        "Common Voice",
        "Welcome to Common Voice",

        "Common Voice",
        "Welcome to Common Voice",

        "published",
        1,

        new Date().toISOString()
    );
}

module.exports = db;
