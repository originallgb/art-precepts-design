# Art Precepts Design

I've been saving things I like on Google Arts & Culture for years:
paintings, maps, furniture, architectural drawings. I wanted to find out
whether that collection could tell me something useful about my taste,
and whether I could turn it into guidance for things I make.

This is that experiment. The aim is a set of `design.md` playbooks for
interfaces, interiors and a wider design language, grounded in the works
I keep returning to.

**Work in progress:** 801 collected works, 800 with generated visual
analysis, and ten provisional groups. The playbooks are still to come.

## How it started

The first attempt was a sketch typed into AI Studio on my phone. It
produced [CuratorMD](apps/curatormd/BUILD_HISTORY.md), an app with artwork
analysis, curatorial themes and a design-token sandbox. My next prompt
restyled it. A later attempt to extend it hit the model quota.

Looking back at the code, I found a more basic problem: the analysis had
been given the artwork's title and metadata, but not the image.

I picked the idea up again as a pipeline. This time the model received
the images, with a prompt asking it to consider composition, utility,
symbolism, space and colour. Each stage became a chance to try a different
approach, inspect the result and work out what to keep.

## A small example

One generated observation about Fernando Botero's *Arcángel* suggests
using a dominant foreground form against a repeating background to create
depth. That gives me something specific to try in an interface, and a
question: does the arrangement help someone find what matters?

[Read the model's analysis](catalogue/0100_arc-ngel_NgHYVFO9OGwDSA.md)
· [See the work at its source](https://artsandculture.google.com/asset/arc%C3%A1ngel/NgHYVFO9OGwDSA)

That translation is the part I still need to test. An observation about
a painting is a starting point, not a proven rule for designing software.

## Where it stands

The [catalogue](catalogue/) contains the generated critiques and design
suggestions. The [cluster map](clusters/latent_cluster_map.svg) is an
exploratory view of ten groups, whose
[methodology remains under review](docs/decisions/001-latent-clustering-methodology.md).
Some apparent connections may reflect artist names and the model's writing
as much as visual relationships.

I selected the collection, set the brief and chose between approaches.
AI tools generated much of the code and analysis. The critiques are the
model's words; the notes also contain scripted text and space for my own
annotations. Those annotations and a worked design example are next.
The original app and recovered [pipeline scripts](pipeline/README.md)
are experimental, with local dependencies, rather than a ready-to-run service.

## Continuing in public

I'm opening up the working record while the project is unfinished. I want
to make the work visible, share what I'm learning and give myself a reason
to keep going. The false starts belong here too.

Follow the [journal and next steps](docs/journal/README.md), browse the
[collection spreadsheet](https://docs.google.com/spreadsheets/d/1Tznbdor6-JFLkGNtuN5StasMSopnLkhdqzgbq7NWdAU/edit),
or read the [longer project history](docs/process/2026-09-24-readme-archive.md).

## Sources and licence

Artwork images are not included. Catalogue notes link to their sources.
Museum-supplied text and metadata retain their own rights and are excluded
from this project's content licence. Code is [MIT](LICENSE); original
writing and generated analysis are covered by the [content licence](LICENSE-content.md).
