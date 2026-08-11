const express = require("express");
const path = require("path");

const db = require("./db");

const app = express();
const PORT = 3000;

// JSON request လက်ခံရန်
app.use(express.json());

// public folder ထဲက HTML/CSS/JS တွေကို serve လုပ်မယ်
app.use(express.static(path.join(__dirname, "public")));


/*
========================================
PUBLIC API
========================================
*/

// User တွေမြင်ရမယ့် Production data
app.get("/api/page", (req, res) => {

    const page = db
        .prepare(`
            SELECT
                production_title AS title,
                production_description AS description,
                updated_at
            FROM pages
            WHERE id = 1
        `)
        .get();

    res.json(page);
});


/*
========================================
ADMIN API
========================================
*/

// Admin dashboard အတွက် data
app.get("/api/admin", (req, res) => {

    const page = db
        .prepare("SELECT * FROM pages WHERE id = 1")
        .get();

    res.json(page);
});


/*
========================================
SAVE DRAFT
========================================
*/

app.post("/api/admin/draft", (req, res) => {

    const {
        title,
        description
    } = req.body;

    if (!title || !description) {

        return res.status(400).json({
            error: "Title နှင့် Description လိုအပ်ပါတယ်။"
        });
    }

    db.prepare(`
        UPDATE pages

        SET
            draft_title = ?,
            draft_description = ?,
            status = 'draft',
            tested = 0,
            updated_at = ?

        WHERE id = 1
    `).run(
        title,
        description,
        new Date().toISOString()
    );

    res.json({
        message: "Draft saved successfully."
    });
});


/*
========================================
TEST
========================================
*/

app.post("/api/admin/test", (req, res) => {

    const page = db
        .prepare(`
            SELECT
                draft_title,
                draft_description
            FROM pages
            WHERE id = 1
        `)
        .get();

    if (!page) {

        return res.status(404).json({
            error: "Page not found."
        });
    }

    db.prepare(`
        UPDATE pages

        SET
            tested = 1,
            status = 'tested'

        WHERE id = 1
    `).run();

    res.json({
        title: page.draft_title,
        description: page.draft_description,

        message: "Test completed."
    });
});


/*
========================================
APPROVE
========================================
*/

app.post("/api/admin/approve", (req, res) => {

    const page = db
        .prepare(`
            SELECT tested
            FROM pages
            WHERE id = 1
        `)
        .get();

    if (!page.tested) {

        return res.status(400).json({
            error: "အရင် Test လုပ်ရပါမယ်။"
        });
    }

    db.prepare(`
        UPDATE pages

        SET status = 'approved'

        WHERE id = 1
    `).run();

    res.json({
        message: "Content approved."
    });
});


/*
========================================
LAUNCH
========================================
*/

app.post("/api/admin/launch", (req, res) => {

    const page = db
        .prepare(`
            SELECT *
            FROM pages
            WHERE id = 1
        `)
        .get();

    if (page.status !== "approved") {

        return res.status(400).json({
            error:
                "Approved ဖြစ်ပြီးမှ Launch လုပ်နိုင်ပါတယ်။"
        });
    }


    /*
    ====================================
    အရေးကြီးဆုံးအပိုင်း
    ====================================

    Draft ကို Production သို့ publish လုပ်ခြင်း
    */

    db.prepare(`
        UPDATE pages

        SET
            production_title = draft_title,
            production_description = draft_description,

            status = 'published',

            updated_at = ?

        WHERE id = 1
    `).run(
        new Date().toISOString()
    );


    res.json({
        message: "🚀 Launch successful."
    });
});


/*
========================================
START SERVER
========================================
*/

app.listen(PORT, () => {

    console.log(`
=================================
Mini CMS is running
=================================

Public:
http://localhost:${PORT}

Admin:
http://localhost:${PORT}/admin.html

=================================
    `);

});
