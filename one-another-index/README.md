# One Another Index

What the New Testament teaches and shows about **treating one another**, **handling conflict**, and **living among unbelievers**, with selected wisdom from Proverbs. Built for community group leaders.

Open `index.html` in any browser on a phone or computer. It is a single page with no sign-in and no app to install. Every reference opens the passage in the ESV on [ESV.org](https://www.esv.org).

## What's inside

- **793 New Testament passages** covering 2,708 of its 7,941 verses, plus **89 proverbs**
- **36 topics** in three categories: One Another (14), Conflict (11), Unbelievers (11)
- **10 situations** to start from, such as *Someone wronged me*, *Two people are at odds* and *Talking with a skeptic*
- **Key passages**, the ones to know first, listed at the top of every topic
- Filters for teaching, examples, parables, proverbs, and Jesus' own words and example
- Links both ways where the New Testament quotes or echoes a proverb

## Using it with a group

1. Start from a situation or a topic.
2. Tap a passage to see its summary, its topics, and a **Read in ESV** button.
3. Tap **Save** on the ones you want to discuss.
4. Open **Saved**, tap **Copy list**, and paste it into your group chat. Each reference in the list links to the passage on ESV.org.

Saved lists stay on the device you saved them on.

### Linking straight to a topic

Add a code to the end of the page address, such as `index.html#forgiveness`.

| Category | Codes |
|---|---|
| One Another | `love` `friendship` `humility` `serve` `encourage` `generosity` `unity` `patience` `speech` `accountability` `prayer` `impartiality` `leaders` `household` |
| Conflict | `forgiveness` `confront` `restore` `anger` `quarrels` `judging` `division` `revenge` `peacemaking` `disputes` `divisive` |
| Unbelievers | `witness` `conduct` `answer` `enemies` `persecution` `authorities` `good` `engaging` `family` `rejection` `boundaries` |
| Situations | `wronged` `at-odds` `correcting` `gray-areas` `sharp-words` `causing-division` `skeptic` `hostility` `unbelieving-family` `leading` |
| Other | `key` `proverbs` `all` `saved` |

## What's included

Passages that teach or show how believers should treat one another, handle conflict, and relate to unbelievers, opponents and governing authorities. Stories count, including cautionary ones, and so do household and workplace instructions. Passages about doctrine, the end times or private devotion are left out unless the text itself draws a point about how to treat people.

Proverbs is a selection, not the whole book: only sayings that speak directly to relationships, conflict and outsiders. They sit in their own section under each topic, after the New Testament. Proverbs describe how life usually works; they are wisdom rather than promises, and some pull against each other on purpose (26:4–5).

## Scripture and copyright

No Bible text is stored in this page or this repository. Every reference links to the English Standard Version on ESV.org, published by Crossway. Crossway's permissions don't allow storing this much ESV text in a reference tool, so the page links to it instead.

The titles and summaries are original study aids, not Scripture. They were drafted with Claude (Anthropic), and every reference was checked against the text. Read each passage itself before teaching from it. References follow ESV verse numbering.

## Editing the passages

The page is generated from three files. Don't edit `index.html` by hand.

| File | What it holds |
|---|---|
| `data/catalog.json` | Every passage, one per line: reference, title, summary, topics and kind |
| `data/books.json` | Chapter and verse counts used to check references |
| `src/template.html` | The page's design and code |
| `build.py` | Checks the catalog and rebuilds `index.html` |

To add or change a passage, edit `data/catalog.json` and run:

```
python3 build.py
```

It needs only Python 3. If a reference doesn't exist or a topic code is misspelled, it lists the problem and leaves `index.html` untouched.

Each entry looks like this:

```json
{"ref":"Matt 18:15-17","title":"Go to them privately first","summary":"...","themes":["cf.confront","cf.restore"],"type":"teaching","jesus":true,"key":true}
```

- **ref**: book code plus chapter and verse, such as `Rom 12:9-13`, `2Cor 6:14-7:1` or `Prov 15:1`. Book codes: `Matt Mark Luke John Acts Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet 2Pet 1John 2John 3John Jude Rev Prov`
- **themes**: one to three topic codes. Use the codes in the table above with their category prefix: `oa.` for One Another, `cf.` for Conflict, `un.` for Unbelievers.
- **type**: `teaching`, `example`, `parable` or `proverb`
- Optional: `key`, `jesus` or `cautionary` set to `true`; `context` for a whole story's range; `parallels` for Gospel parallels; `note` for a short caution; `xref` for New Testament and Proverbs links

## Putting it online

To give the group a public link, turn on GitHub Pages for this repository: **Settings → Pages → Deploy from a branch → `main` / (root)**. After a minute the index will be at `https://tarsmahan26.github.io/TCC-Community-Groups/one-another-index/`.
