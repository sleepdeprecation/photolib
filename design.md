# photolib design

_Note_: this is currently more of a collection of thoughts than a formal design specification.

## End Goal

-   GUI Application for managing a library of photos
    -   CROSS PLATFORM
    -   By default displays a grid of photos
    -   Can zoom in on an individual photo

-   Library Management
    -   **Assumption**: sole owner of the library directory
    -   Can add arbitrary tags to images
        -   Can view all images with tag
    -   Has some concept of a "container" of JPG+RAW file
        -   Container could also maybe include edits done outside of application?

-   Export to external services
    -   Instagram
    -   500px

### Outside of Scope

This application is, at least currently, being purpose built for my own photo management needs.
As such, there are a number of things that I consider out of scope based on my current workflow.
Things currently considered out of scope can eventually be brought in scope if other people are interested in them,
or if someone else wants to pick up that work.

-   Any photo editing
    -   **Rationale**: I already have tools that I use for editing photos.
        For the most part I'm pretty comfortable with them, and don't think it's worth trying to tack on extra features, because other applications already do photo editing really well (and are purpose built for that task).
    -   **Exceptions**: It might be fun to develop some default filters like Instagram and add them in, for extra shenanigans.

## Technical Thoughts

-   This will probably use a sqlite database, for portability
-   QT seems like the "best" cross-platform UI toolkit
    -   Though, I'm also not opposed to writing multiple UI layers.
        -   Multiple layers would allow for better OS integration (look-wise at least)
