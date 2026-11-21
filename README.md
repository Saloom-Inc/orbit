# Open CAD Library

An open-source, single-page library of public **FTC & FRC robot CAD**: 254 CAD files and 13 resources. You can browse by program, season, mechanism and CAD platform (Onshape, Fusion 360, GrabCAD, Google Drive).

It has no backend, no build tooling and no tracking. It is one static `index.html` that works on GitHub Pages, Netlify, Vercel or any file host.

## Features
- CAD files / Resources tabs, with counts
- Search across titles, team numbers, mechanisms and hosts
- Filters for program, season, category and platform, with live counts
- Sorting: newest season, oldest season, A–Z, Z–A, library order
- Favorites and dark mode, saved in your browser
- A "Submit to library" form that generates a ready-to-paste data line
- Each card gets a line drawing of its mechanism, so no third-party thumbnails are needed

## Project layout
```
data/library.txt    ← the whole dataset, one entry per line (edit this)
src/template.html   ← page, styles and script
build.py            ← merges the two into index.html
index.html          ← built site (deploy this)
```

## Data format
`kind|title|url|program|season|tags|platform`

| field | values |
|---|---|
| kind | empty = CAD file, `R` = resource |
| url | full URL; `~` is shorthand for `https://cad.onshape.com/documents/` |
| program | empty = FTC, or `FRC` |
| season | `B` Biobuzz 26-27, `D` Decode 25-26, `I` Into the Deep 24-25, `C` Centerstage 23-24, `P` Power Play 22-23, `F` Freight Frenzy 21-22, `S` Skystone 19-20, `U` Unspecified/Offseason |
| tags | one base-36 character per category, the first is the primary: 0 Full Robot, 1 Mecanum, 2 Tank, 3 Swerve Drive, 4 Intake, 5 Claw/Gripper, 6 Linear Slides/Extension, 7 Turret, 8 Shooter, 9 Undershooter, a Counter Roller Shooter, b Differential/PTO, c Vector Wheel, d Number Plate/Misc, e Misc, f Other |
| platform | `o` Onshape, `f` Fusion 360, `g` GrabCAD, `d` Google Drive, `x` Other |

## Add an entry
1. Open the site and click **Submit to library**, then copy the generated line. You can also write the line by hand.
2. Add it to `data/library.txt`.
3. Run `python3 build.py` and open a pull request.

## Credits
The link index was first compiled at [cadbaseftc.com](https://www.cadbaseftc.com/) by FTC team 31071 Stratos. Every CAD design belongs to the team that published it. This project only links to their public files.

## License
MIT for the code (see `LICENSE`). The linked CAD files keep their authors' own terms.
