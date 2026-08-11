const express = require("express");
const path = require("path");
const db = require("./db");

const app = express();

const PORT = process.env.PORT || 3000;

app.use(express.json());


// ================================
// HTML FILES
// ================================

app.use(express.static(__dirname));


// ================================
// PUBLIC API
// ================================

app.get("/api/page", (req, res) => {

    const page = db.prepare(`
        SELECT
            production_title AS title,
            production_description AS description
        FROM pages
        WHERE id = 1
    `).get();

    res.json(page);
});


// ================================
// ADMIN API
// ================================

app.get("/api/admin", (req, res) => {

    const page = db
        .prepare("SELECT * FROM pages WHERE id = 1")
        .get();

    res.json(page);
});


// ================================
// SAVE DRAFT
// ================================

app.post("/api/H/draft", (req, res) => {

    const {
        title,
        description
    } = req.body;

    if (!title || !description) {

        return res.status(400).json({
            error: "Title and description are required."
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
        message: "Draft saved."
    });
});


// ================================
// TEST
// ================================

app.post("/api/H/test", (req, res) => {

    const page = db.prepare(`
        SELECT
            draft_title,
            draft_description
        FROM pages
        WHERE id = 1
    `).get();

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


// ================================
// APPROVE
// ================================

app.post("/api/H/approve", (req, res) => {

    const page = db
        .prepare(`
            SELECT tested
            FROM pages
            WHERE id = 1
        `)
        .get();

    if (!page.tested) {

        return res.status(400).json({
            error: "Test must be completed first."
        });
    }

    db.prepare(`
        UPDATE pages

        SET status = 'approved'

        WHERE id = 1
    `).run();

    res.json({
        message: "Approved."
    });
});


// ================================
// LAUNCH
// ================================

app.post("/api/H/launch", (req, res) => {

    const page = db
        .prepare(`
            SELECT *
            FROM pages
            WHERE id = 1
        `)
        .get();

    if (page.status !== "approved") {

        return res.status(400).json({
            error: "Content must be approved first."
        });
    }

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
        message: "🚀 Published successfully."
    });
});


// ================================
// START
// ================================

app.listen(PORT, "0.0.0.0", () => {

    console.log(
        `CMS server running on port ${PORT}`
    );

});
