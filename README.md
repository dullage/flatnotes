![Logo](docs/logo.svg)

A database-less note taking web app that utilises a flat folder of markdown files for storage.

Log into the [demo site](https://demo.flatnotes.io) and take a look around. The username is `demo` and the password is `demo`. *Note: This site resets every 15 minutes.*


## Design Principle

flatnotes is designed to be a distraction free note taking app that puts your note content first. This means:

* A clean and simple user interface.
* No folders, categories, keywords, notebooks, tags or anything like that. Just all of your notes backed by powerful search functionality.
* Quick access to a full text search from anywhere in the app (keyboard shortcut "/").


## Q&A
### Where is the database?
There is no database, only a single folder of markdown files (and the .flatnotes sub-folder).

### What is the .flatnotes sub-folder for?
This stores a full text index of your note content allowing for rapid search times.

### Can I delete the .flatnotes sub-folder?
As long as flatnotes isn't running, sure! It'll just get rebuilt then next time flatnotes is run.

### Can I add, edit & delete the markdown files outside of flatnotes?
Yup. The only thing flatnotes caches is the search index and that's synced on every search (and when flatnotes first starts).

### Can I perform advanced searches?
Yes! See the [Advanced Searching](https://github.com/Dullage/flatnotes/wiki/Advanced-Searching) wiki page.

### How do I get my notes out of flatnotes?
They're just markdown files. There's no database, proprietary formatting, complicated folder structures or anything like that so you're free to just move the files elsewhere and use another markdown editor.

### Is there an API?
Yes. The docs are available at the `/docs` endpoint. See [demo.flatnotes.io/docs](https://demo.flatnotes.io/docs) as an example.


## Roadmap
I want to keep flatnotes as simple and distraction free as possible which means limiting new features. This said, I welcome feedback and suggestions.

One feature I do plan to implement is the ability to *share* a note. In the spirit of simple and database-less, the current plan is to generate temporary pre-signed URLs but this needs to be explored.


## Thanks

A special thanks to 2 fantastic open source projects that make flatnotes possible.

* [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) - A fast, pure Python search engine library.
* [TOAST UI Editor](https://ui.toast.com/tui-editor) - A GFM Markdown and WYSIWYG editor for the browser.
