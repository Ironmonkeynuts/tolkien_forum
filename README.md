[![screenshot](documentation/forum-logo-hero.png)](https://imn-project-tolkienforum-ed83da8fbf63.herokuapp.com)

Developer: David Doyle-Owen ([Ironmonkeynuts](https://www.github.com/Ironmonkeynuts))

[![GitHub commit activity](https://img.shields.io/github/commit-activity/t/Ironmonkeynuts/tolkien_forum)](https://www.github.com/Ironmonkeynuts/tolkien_forum/commits/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/Ironmonkeynuts/tolkien_forum)](https://www.github.com/Ironmonkeynuts/tolkien_forum/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/Ironmonkeynuts/tolkien_forum)](https://www.github.com/Ironmonkeynuts/tolkien_forum)

A fully functional community-driven Django web forum inspired by J.R.R. Tolkien’s world. Users can discuss Middle-earth lore, post articles, comment, and apply for elevated roles in a secure and moderated environment.

Speak, Friend and Enter is an online forum dedicated to celebrating the rich and timeless works of J.R.R. Tolkien. From The Lord of the Rings and The Hobbit to The Silmarillion and his vast legendarium, this community offers a welcoming space where fans, scholars, and newcomers alike can gather to discuss, explore, and appreciate Tolkien’s enduring legacy. Whether you are here to debate the finer points of Elvish linguistics, analyze the themes of heroism and loss, or simply share your favorite moments from the books or films, you will find kindred spirits within our fellowship.

Our aim is to foster thoughtful, respectful, and engaging discussion about all aspects of Tolkien’s world. We encourage contributions from a wide range of perspectives — literary analysis, artistic interpretations, adaptations in film and media, gaming, and creative works inspired by Middle-earth. We provide dedicated sections for lore deep-dives, fan fiction, art galleries, language studies, and real-world influences on Tolkien’s writing. By bringing together enthusiasts of varied backgrounds, we hope to create a vibrant community that honors Tolkien’s spirit of fellowship, discovery, and wonder.

At Speak, Friend and Enter, our mission is simple: to build a safe, inclusive, and inspiring space where the magic of Tolkien’s universe can thrive for generations to come. We are committed to maintaining a positive atmosphere where members can learn, share, and connect through their love of Middle-earth and beyond. Whether you are embarking on your first journey through the Shire or have long walked the paths of Beleriand, we invite you to join our fellowship — where all who speak, friend, may enter.

![screenshot](documentation/mockup.png)

source: [tolkien_forum amiresponsive](https://ui.dev/amiresponsive?url=https://imn-project-tolkienforum-ed83da8fbf63.herokuapp.com)

## UX

### The 5 Planes of UX

#### 1. Strategy

**Purpose**
- Provide content creators with tools to create, manage, and moderate engaging forum content and user interactions.
- Offer users and guests an intuitive platform to explore, engage, and contribute to forum discussions.

**Primary User Needs**
- Content creators need seamless tools for publishing and managing articles.
- Admin and moderators need seemless tools for managing and moderating profiles and content.
- Registered users need the ability to engage with forum content through comments and account features.
- Guests need the ability to browse and enjoy forum content without registration.

**Business Goals**
- Foster a dynamic forum platform with active user participation.
- Build a sense of community through discussions and user engagement.
- Ensure easy forum content management for owners.

#### 2. Scope

**[Features](#features)** (see below)

**Content Requirements**
- Forum article management (create, update, delete, and preview).
- Content moderation and management tools.
- User account features (register, log in, write/edit/delete comments).
- Notification system for content approval status.
- 404 error page for lost users.

#### 3. Structure

**Information Architecture**
- **Navigation Menu**:
  - Links to Welcome, Forum articles, Login/Register, and Dashboard (for moderators and admin).
- **Hierarchy**:
  - Forum content displayed prominently for easy browsing.
  - Clear call-to-action buttons for account creation and engagement (e.g., commenting).

**User Flow**
1. Guest users browse forum content → read articles and see commenter names.
2. Guest users register for an account → become a Member, gain a profile and log in to leave comments.
3. Members leave comments → receive a pending approval notification.
4. Members view own profile → add an avatar and write a bio.
5. Members browse community profiles of other members → read bios and view articles of profiles belonging to Content Creators
5. Members apply to be Content Creators → receive a pending approval notification.
6. Content Creators create, update, and manage articles → present ideas to start fresh conversations.
7. Content Creators view existing own articles in profile → edit own articles.
8. Members and Content Creators apply to become a Moderator → receive a pending approval notification.
9. Moderators and Admin approve or disapprove articles, comments and profiles → manage user interactions.

#### 4. Skeleton

**[Wireframes](#wireframes)** (see below)

#### 5. Surface

**Visual Design Elements**
- **[Colours](#colour-scheme)** (see below)
- **[Typography](#typography)** (see below)

### Colour Scheme

I used [Bootstrap 5 ](https://getbootstrap.com/docs/5.0/utilities/colors/) to generate my color scheme.

- `text-warning` primary text.
- `` primary highlights.
- `text-light` secondary text.
- `bg-dark` primary background
- `bg-success` secondary background

![screenshot](documentation/bootstrap-colors.png)

### Typography

- [Bootstrap Font stack - $font-family-sans-serif](https://getbootstrap.com/docs/5.0/content/reboot/#native-font-stack) was used for all text. This stack adapts to device and browser type applied throughout the <body>.


## Wireframes

To follow best practice, wireframes were developed for mobile, tablet, and desktop sizes.
I've used [Balsamiq](https://balsamiq.com/wireframes) to design my site wireframes.

| Page | Mobile | Tablet | Desktop |
| --- | --- | --- | --- |
| Register | ![screenshot](documentation/wireframes/register-mobile.png) | ![screenshot](documentation/wireframes/register-tablet.png) | ![screenshot](documentation/wireframes/register-desktop.png) |
| Login | ![screenshot](documentation/wireframes/login-mobile.png) | ![screenshot](documentation/wireframes/login-tablet.png) | ![screenshot](documentation/wireframes/login-desktop.png) |
| Welcome | ![screenshot](documentation/wireframes/welcome-mobile.png) | ![screenshot](documentation/wireframes/welcome-tablet.png) | ![screenshot](documentation/wireframes/welcome-desktop.png) |
| Forum | ![screenshot](documentation/wireframes/forum-mobile.png) | ![screenshot](documentation/wireframes/forum-tablet.png) | ![screenshot](documentation/wireframes/forum-desktop.png) |
| Add/Edit Article | ![screenshot](documentation/wireframes/edit-article-mobile.png) | ![screenshot](documentation/wireframes/edit-article-tablet.png) | ![screenshot](documentation/wireframes/edit-article-desktop.png) |
| Article Detail | ![screenshot](documentation/wireframes/article-detail-mobile.png) | ![screenshot](documentation/wireframes/article-detail-tablet.png) | ![screenshot](documentation/wireframes/article-detail-desktop.png) |
| Profile | ![screenshot](documentation/wireframes/profile-mobile.png) | ![screenshot](documentation/wireframes/profile-tablet.png) | ![screenshot](documentation/wireframes/profile-desktop.png) |
| Community | ![screenshot](documentation/wireframes/community-mobile.png) | ![screenshot](documentation/wireframes/community-tablet.png) | ![screenshot](documentation/wireframes/community-desktop.png) |
| Contact | ![screenshot](documentation/wireframes/contact-mobile.png) | ![screenshot](documentation/wireframes/contact-tablet.png) | ![screenshot](documentation/wireframes/contact-desktop.png) |
| 404 | ![screenshot](documentation/wireframes/404-mobile.png) | ![screenshot](documentation/wireframes/404-tablet.png) | ![screenshot](documentation/wireframes/404-desktop.png) |

## User Stories

| Target | Expectation | Outcome |
| --- | --- | --- |
| As a site user | I can view a list of articles | so that I can choose content to read. |
| As a site user | I can filter articles by title, author or date created | so that I may view a filtered sample of articles. |
| As a site user | I can click on an article | so that I can read the full text. |
| As a site user | I can view comments made about articles | so that I may read the discussion so far. |
| As a site user | I can see author and timestamp on articles and comments | so that I can see who created content and when it was created. |
| As a site user | I can contact the site admin | so that we can discuss collaboration or other topic. |
| As a site user | I  can register to become an member of the site | so that I can comment on articles and take part in discussion. |
| As a registered user | I would like to log in to the site | so that I can leave comments on forum articles. |
| As a registered user | I can comment on an article | so that I can add to the discussion. |
| As a registered user | I can edit or delete my comment | so that I may modify the content. |
| As a registered user | I can apply to become a Content Creator | so that I may post articles in addition to member permissions. |
| As a registered user | I can apply to become a Moderator | so that I can enforce the site rules. |
| As a content creator | I can create, read, update and delete own articles with a title, featured image, and content | so that I can share my experiences with my audience. |
| As a content creator | I can create draft articles | so that I can finish writing the content later. |
| As a content creator | I can view a list of all my published forum articles | so that I can manage them from profile |
| As a moderator/admin | I can create, read, update, delete and moderate articles | so that I can manage the content of the site. |
| As a site user | I can see a 404 error page if I get lost | so that it's obvious that I've stumbled upon a page that doesn't exist. | 
Future:
| As a moderator or admin | I can block a member | so that the member may not make comments. |
| As an admin | I can suspend a member | so that they may not access the forum temporarily. |
| As an admin | I can reinstate a member | so that they may access the forum again. | 
| As a moderator or admin | I can unblock a member| so that the member may make comments again. |
| As a content creator | I would like to view a list of all comments (both approved and pending) | so that I can manage user engagement effectively. |
| As a content creator | I can upload prepared text file to my article | so that it is easier to add large amounts of text. |
| As an admin | I can delete and ban a member | so that they may not access the forum permanantly. |
| As a site owner | I can give or remove site admin permissions to a member | so that they can manage the site. |
| As an admin | I can verify email of users on registration | so that I can ensure users can recieve password reset emails. |
| As a moderator | I can block a member for a fixed period | so that |
| As a registered user | I can report an article or comment as breaking the site rules | so that suspected undesirable content is reviewed for removal. |


## Features

### Existing Features

| Feature | Notes | Screenshot |
| --- | --- | --- |
| Register | Authentication is handled by allauth, allowing users to register accounts. | ![screenshot](documentation/features/register.png) |
| Login | Authentication is handled by allauth, allowing users to log in to their existing accounts. | ![screenshot](documentation/features/login.png) |
| Logout | Authentication is handled by allauth, allowing users to log out of their accounts. | ![screenshot](documentation/features/logout.png) |
| Forum | The forum page displays basic information about forum articles, including image, title, author, date, and a brief excerpt. | ![screenshot](documentation/features/forum.png) |
| View article | Users can view the full forum article details, including any comments. | ![screenshot](documentation/features/view-article.png) |
| Pagination | forum articles are displayed in pages, with six articles per page. This provides better navigation for users through the article list. | ![screenshot](documentation/features/pagination.png) |
| Add Comments | Authenticated visitors can comment on forum articles; comments require approval before being published. | ![screenshot](documentation/features/add-comment.png) |
| Edit Comments | Authenticated visitors can edit their own comments. | ![screenshot](documentation/features/edit-comment.png) |
| Delete Comments | Authenticated visitors can delete their own comments. | ![screenshot](documentation/features/delete-comment.png) |
| Content Approvals | Admins can approve or disapprove articles, comments and profiles submitted by users. By default they are visible on the website. | ![screenshot](documentation/features/comment-approval.png) |
| Create article | Content Creators can create/publish forum articles, including setting a featured image using Cloudinary. | ![screenshot](documentation/features/create-article.png) |
| Update article | Content Creators can update/manage their forum articles. | ![screenshot](documentation/features/update-article.png) |
| Delete article | Content Creators can delete forum articles. | ![screenshot](documentation/features/delete-article.png) |
| Manage Forum | Site Admin can manage users, articles, and profiles from the Django admin dashboard. | ![screenshot](documentation/features/manage-forum.png) |
| About Page | The About page displays the scope, aims and mission statement of the forum website | ![screenshot](documentation/features/about.png) |
| Contact Page | A page for users to communicate with the admin of the site. | ![screenshot](documentation/features/contact.png) |
| Contact Messages | Visitors can submit messages along with their email, which are later reviewed by the admin. | ![screenshot](documentation/features/contact-messages.png) |
| Creator Application | Authenticated users can submit an application with reasons, which are later reviewed by the admin or moderators. | ![screenshot](documentation/features/creator-application.png) |
| Moderator Application | Authenticated users can submit an application with reasons, which are later reviewed by the admin. | ![screenshot](documentation/features/creator-application.png) |
| Moderator Dashboard | Authenticated authorised users can review messages and applications. They can also  approve/disapprove application for roles. | ![screenshot](documentation/features/moderator-dashboard.png) |
| View Profile | The Profile page displays the username, user type, avatar and bio of a users profile. Email is visible only to the profile owner and admin | ![screenshot](documentation/features/profile.png) |
| Community Page | The Community page lists the profiles of all registered users showing username, avatar and bio snippet of a users profile. | ![screenshot](documentation/features/community.png) |
| User Feedback | Clear and obvious Django messages are used to provide feedback to user actions. | ![screenshot](documentation/features/messages.png) |
| Heroku Deployment | The site is fully deployed to Heroku, making it accessible online and easy to manage. | ![screenshot](documentation/features/heroku.png) |
| 404 | The 404 error page will indicate when a user has navigated to a page that doesn't exist, replacing the default Heroku 404 page with one that ties into the site's look and feel. | ![screenshot](documentation/features/404.png) |

### Future Features

- **Article Categories/Tags**: Allow users to categorize and tag forum articles, making it easier for visitors to filter content based on their interests.
- **Article Likes/Dislikes or Upvotes**: Implement a "like" or "upvote" system for forum articles to encourage user engagement and give feedback to the author.
- **Comment Replies & Threads**: Enable users to reply to comments, creating nested comment threads for better discussions.
- **Article Sharing**: Add social media sharing buttons (e.g., Twitter, Facebook, LinkedIn) for users to share forum articles.
- **Notifications**: Implement a notification system that alerts users when their comments are approved, when new comments are made on a article they've commented on, or when new articles are published.
- **Email Subscriptions**: Allow users to subscribe to receive email notifications for new articles, updates, or newsletters.
- **Article Analytics**: Provide Article authors with analytics such as views, time spent reading, and engagement rates.
- **Multilingual Support**: Add the ability to write and view forum articles in multiple languages, broadening the audience.
- **Related articles Recommendations**: Show related articles at the bottom of a forum article to encourage further reading and keep users engaged.
- **Content Flagging/Reporting**: Allow users to flag or report inappropriate content (comments or articles) for moderation.
- **SEO Optimization**: Implement features for SEO, such as meta tags, custom URLs, and keywords for better search engine ranking.
- **User Dashboard**: Provide users with a dashboard to track their activity, such as comments made, likes received, and forum articles they’ve interacted with.
- **Admin Dashboard Analytics**: Provide site admins with an analytics dashboard showing user activity, popular articles, most commented articles, etc.
- **Custom Themes for Users**: Allow users to customize the visual theme of the site (colors, fonts, etc.) to suit their preferences.

## Tools & Technologies

| Tool / Tech | Use |
| --- | --- |
| [![badge](https://img.shields.io/badge/Markdown_Builder-grey?logo=markdown&logoColor=000000)](https://markdown.2bn.dev) | Generate README and TESTING templates. |
| [![badge](https://img.shields.io/badge/Git-grey?logo=git&logoColor=F05032)](https://git-scm.com) | Version control. (`git add`, `git commit`, `git push`) |
| [![badge](https://img.shields.io/badge/GitHub-grey?logo=github&logoColor=181717)](https://github.com) | Secure online code storage. |
| [![badge](https://img.shields.io/badge/VSCode-grey?logo=htmx&logoColor=007ACC)](https://code.visualstudio.com) | Local IDE for development. |
| [![badge](https://img.shields.io/badge/HTML-grey?logo=html5&logoColor=E34F26)](https://en.wikipedia.org/wiki/HTML) | Main site content and layout. |
| [![badge](https://img.shields.io/badge/CSS-grey?logo=css&logoColor=1572B6)](https://en.wikipedia.org/wiki/CSS) | Design and layout. |
| [![badge](https://img.shields.io/badge/JavaScript-grey?logo=javascript&logoColor=F7DF1E)](https://www.javascript.com) | User interaction on the site. |
| [![badge](https://img.shields.io/badge/Python-grey?logo=python&logoColor=3776AB)](https://www.python.org) | Back-end programming language. |
| [![badge](https://img.shields.io/badge/Heroku-grey?logo=heroku&logoColor=430098)](https://www.heroku.com) | Hosting the deployed back-end site. |
| [![badge](https://img.shields.io/badge/Bootstrap-grey?logo=bootstrap&logoColor=7952B3)](https://getbootstrap.com) | Front-end CSS framework for modern responsiveness and pre-built components. |
| [![badge](https://img.shields.io/badge/Django-grey?logo=django&logoColor=092E20)](https://www.djangoproject.com) | Python framework for the site. |
| [![badge](https://img.shields.io/badge/PostgreSQL-grey?logo=postgresql&logoColor=4169E1)](https://www.postgresql.org) | Relational database management. |
| [![badge](https://img.shields.io/badge/Cloudinary-grey?logo=cloudinary&logoColor=3448C5)](https://cloudinary.com) | Online static file storage. |
| [![badge](https://img.shields.io/badge/WhiteNoise-grey?logo=python&logoColor=FFFFFF)](https://whitenoise.readthedocs.io) | Serving static files with Heroku. |
| [![badge](https://img.shields.io/badge/Balsamiq-grey?logo=barmenia&logoColor=CE0908)](https://balsamiq.com/wireframes) | Creating wireframes. |
| [![badge](https://img.shields.io/badge/ChatGPT-grey?logo=openai&logoColor=75A99C)](https://chat.openai.com) | Help debug, troubleshoot, and explain things. |
| [![badge](https://img.shields.io/badge/W3Schools-grey?logo=w3schools&logoColor=04AA6D)](https://www.w3schools.com) | Tutorials/Reference Guide |
| [![badge](https://img.shields.io/badge/StackOverflow-grey?logo=stackoverflow&logoColor=F58025)](https://stackoverflow.com) | Troubleshooting and Debugging |

## Database Design

### Data Model

Entity Relationship Diagrams (ERD) help to visualize database architecture before creating models. Understanding the relationships between different tables can save time later in the project.

![screenshot](documentation/erd.png)


I have used `Mermaid` to generate an interactive ERD of my project.
```mermaid
erDiagram

    USER ||--o{ ARTICLE : writes
    USER ||--o{ COMMENT : makes
    USER ||--|| PROFILE : has
    USER ||--o{ CREATORAPPLICATION : submits
    USER ||--o{ MODERATORAPPLICATION : submits

    ARTICLE ||--o{ COMMENT : contains

    ARTICLE {
        int id PK
        string title
        slug slug
        text content
        text excerpt
        image primary_image
        string primary_image_fit
        datetime created_on
        datetime updated_on
        int status
        boolean approved
    }

    COMMENT {
        int id PK
        text body
        datetime created_on
        boolean approved
    }

    PROFILE {
        int id PK
        image avatar
        string avatar_fit
        text bio
        string user_type
        datetime created_on
        boolean approved
    }

    CONTACTMESSAGE {
        int id PK
        email email
        text message
        datetime created_on
        boolean read
    }

    CREATORAPPLICATION {
        int id PK
        text reason
        datetime created_on
        boolean approved
        boolean reviewed
    }

    MODERATORAPPLICATION {
        int id PK
        text reason
        datetime created_on
        boolean approved
        boolean reviewed
    }
```

source: [Mermaid](https://mermaid.live/edit#pako:eNqNUstuwjAQ_BVrz6EiVIiSG21zg9LyuFSRkImXxGpsR45TkQb-vU4C5REq4Yut2dnZnfWWECqG4AHqV04jTUUgiT3LuT8ju12no0ryPp0viEcCoLmJlc4CaHNeppOJ_9bQQiUESoMnZq1wgxnTS0rZvKuTGc1lRAw3CbbQLMmjExgmKmdcUl2QDVKTa2QrLmh0lmdwa0iobFPSXKG4DVGnZyijBg0XSEJt1ayWkjeCecpaQS6N7dB2kDXYvrmOjsurymvFijvLrpVKCE1Trb6RXYiPnqfLOwZ3NiMrsuEJ3jeif_3-eRuPbQuz0cKf-R9L_-YnSiraf4iC8uSqvMAsu2iq9m3ncfQMDgjUNpPZla0LBWBitPJQ7ROj-qtaqIpnl1XNCxmCZ3SODjQGDksO3oYmmUVTKsErYQue-zR8cN2B2-t3h73BY2_Qd6AAr7t34Ecpm-HW7M_63UhqlUfxQWr_C_zI_7I)

## Agile Development Process

### GitHub Projects

[GitHub Projects](https://www.github.com/Ironmonkeynuts/tolkien_forum/projects) served as an Agile tool for this project. Through it, EPICs, User Stories, issues/bugs, and Milestone tasks were planned, then subsequently tracked on a regular basis using the Kanban project board.

![screenshot](documentation/gh-projects.png)

### GitHub Issues

[GitHub Issues](https://www.github.com/Ironmonkeynuts/tolkien_forum/issues) served as an another Agile tool. There, I managed my User Stories and Milestone tasks, and tracked any issues/bugs.

| Link | Screenshot |
| --- | --- |
| [![GitHub issues](https://img.shields.io/github/issues/Ironmonkeynuts/tolkien_forum)](https://www.github.com/Ironmonkeynuts/tolkien_forum/issues) | ![screenshot](documentation/gh-issues-open.png) |
| [![GitHub closed issues](https://img.shields.io/github/issues-closed/Ironmonkeynuts/tolkien_forum)](https://www.github.com/Ironmonkeynuts/tolkien_forum/issues?q=is%3Aissue+is%3Aclosed) | ![screenshot](documentation/gh-issues-closed.png) |

### MoSCoW Prioritization

I've decomposed my Epics into User Stories for prioritizing and implementing them. Using this approach, I was able to apply "MoSCoW" prioritization and labels to my User Stories within the Issues tab.

- **Must Have**: guaranteed to be delivered - required to Pass the project (*max ~60% of stories*)
- **Should Have**: adds significant value, but not vital (*~20% of stories*)
- **Could Have**: has small impact if left out (*the rest ~20% of stories*)
- **Won't Have**: not a priority for this iteration - future features

## Testing

> [!NOTE]
> For all testing, please refer to the [TESTING.md](TESTING.md) file.

## Deployment

The live deployed application can be found deployed on [Heroku](https://imn-project-tolkienforum-ed83da8fbf63.herokuapp.com).

### Heroku Deployment

This project uses [Heroku](https://www.heroku.com), a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

Deployment steps are as follows, after account setup:

- Select **New** in the top-right corner of your Heroku Dashboard, and select **Create new app** from the dropdown menu.
- Your app name must be unique, and then choose a region closest to you (EU or USA), then finally, click **Create App**.
- From the new app **Settings**, click **Reveal Config Vars**, and set your environment variables to match your private `env.py` file.

> [!IMPORTANT]
> This is a sample only; you would replace the values with your own if cloning/forking my repository.

| Key | Value |
| --- | --- |
| `CLOUDINARY_URL` | user-inserts-own-cloudinary-url |
| `DATABASE_URL` | user-inserts-own-postgres-database-url |
| `DISABLE_COLLECTSTATIC` | 1 (*this is temporary, and can be removed for the final deployment*) |
| `SECRET_KEY` | any-random-secret-key |

Heroku needs some additional files in order to deploy properly.

- [requirements.txt](requirements.txt)
- [Procfile](Procfile)
- [.python-version](.python-version)

You can install this project's **[requirements.txt](requirements.txt)** (*where applicable*) using:

- `pip3 install -r requirements.txt`

If you have your own packages that have been installed, then the requirements file needs updated using:

- `pip3 freeze --local > requirements.txt`

The **[Procfile](Procfile)** can be created with the following command:

- `echo web: gunicorn app_name.wsgi > Procfile`
- *replace `app_name` with the name of your primary Django app name; the folder where `settings.py` is located*

The **[.python-version](.python-version)** file tells Heroku the specific version of Python to use when running your application.

- `3.12` (or similar)

For Heroku deployment, follow these steps to connect your own GitHub repository to the newly created app:

Either (*recommended*):

- Select **Automatic Deployment** from the Heroku app.

Or:

- In the Terminal/CLI, connect to Heroku using this command: `heroku login -i`
- Set the remote for Heroku: `heroku git:remote -a app_name` (*replace `app_name` with your app name*)
- After performing the standard Git `add`, `commit`, and `push` to GitHub, you can now type:
	- `git push heroku main`

The project should now be connected and deployed to Heroku!

### Cloudinary API

This project uses the [Cloudinary API](https://cloudinary.com) to store media assets online, due to the fact that Heroku doesn't persist this type of data.

To obtain your own Cloudinary API key, create an account and log in.

- For "Primary Interest", you can choose **Programmable Media for image and video API**.
- *Optional*: edit your assigned cloud name to something more memorable.
- On your Cloudinary Dashboard, you can copy your **API Environment Variable**.
- Be sure to remove the leading `CLOUDINARY_URL=` as part of the API **value**; this is the **key**.
    - `cloudinary://123456789012345:AbCdEfGhIjKlMnOpQrStuVwXyZa@1a2b3c4d5)`
- This will go into your own `env.py` file, and Heroku Config Vars, using the **key** of `CLOUDINARY_URL`.

### PostgreSQL

This project uses a [Code Institute PostgreSQL Database](https://dbs.ci-dbs.net) for the Relational Database with Django.

> [!CAUTION]
> - PostgreSQL databases by Code Institute are only available to CI Students.
> - You must acquire your own PostgreSQL database through some other method if you plan to clone/fork this repository.
> - Code Institute students are allowed a maximum of 8 databases.
> - Databases are subject to deletion after 18 months.

To obtain my own Postgres Database from Code Institute, I followed these steps:

- Submitted my email address to the CI PostgreSQL Database link above.
- An email was sent to me with my new Postgres Database.
- The Database connection string will resemble something like this:
    - `postgres://<db_username>:<db_password>@<db_host_url>/<db_name>`
- You can use the above URL with Django; simply paste it into your `env.py` file and Heroku Config Vars as `DATABASE_URL`.

### WhiteNoise

This project uses the [WhiteNoise](https://whitenoise.readthedocs.io/en/latest/) to aid with static files temporarily hosted on the live Heroku site.

To include WhiteNoise in your own projects:

- Install the latest WhiteNoise package:
    - `pip install whitenoise`
- Update the `requirements.txt` file with the newly installed package:
    - `pip freeze --local > requirements.txt`
- Edit your `settings.py` file and add WhiteNoise to the `MIDDLEWARE` list, above all other middleware (apart from Django’s "SecurityMiddleware"):

```python
# settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # any additional middleware
]
```


### Local Development

This project can be cloned or forked in order to make a local copy on your own system.

For either method, you will need to install any applicable packages found within the [requirements.txt](requirements.txt) file.

- `pip3 install -r requirements.txt`.

You will need to create a new file called `env.py` at the root-level, and include the same environment variables listed above from the Heroku deployment steps.

> [!IMPORTANT]
> This is a sample only; you would replace the values with your own if cloning/forking my repository.

Sample `env.py` file:

```python
import os

os.environ.setdefault("SECRET_KEY", "any-random-secret-key")
os.environ.setdefault("DATABASE_URL", "user-inserts-own-postgres-database-url")
os.environ.setdefault("CLOUDINARY_URL", "user-inserts-own-cloudinary-url")  # only if using Cloudinary

# local environment only (do not include these in production/deployment!)
os.environ.setdefault("DEBUG", "True")
```

Once the project is cloned or forked, in order to run it locally, you'll need to follow these steps:

- Start the Django app: `python3 manage.py runserver`
- Stop the app once it's loaded: `CTRL+C` (*Windows/Linux*) or `⌘+C` (*Mac*)
- Make any necessary migrations: `python3 manage.py makemigrations --dry-run` then `python3 manage.py makemigrations`
- Migrate the data to the database: `python3 manage.py migrate --plan` then `python3 manage.py migrate`
- Create a superuser: `python3 manage.py createsuperuser`
- Load fixtures (*if applicable*): `python3 manage.py loaddata file-name.json` (*repeat for each file*)
- Everything should be ready now, so run the Django app again: `python3 manage.py runserver`

If you'd like to backup your database models, use the following command for each model you'd like to create a fixture for:

- `python3 manage.py dumpdata your-model > your-model.json`
- *repeat this action for each model you wish to backup*
- **NOTE**: You should never make a backup of the default *admin* or *users* data with confidential information.

#### Cloning

You can clone the repository by following these steps:

1. Go to the [GitHub repository](https://www.github.com/Ironmonkeynuts/tolkien_forum).
2. Locate and click on the green "Code" button at the very top, above the commits and files.
3. Select whether you prefer to clone using "HTTPS", "SSH", or "GitHub CLI", and click the "copy" button to copy the URL to your clipboard.
4. Open "Git Bash" or "Terminal".
5. Change the current working directory to the location where you want the cloned directory.
6. In your IDE Terminal, type the following command to clone the repository:
	- `git clone https://www.github.com/Ironmonkeynuts/tolkien_forum.git`
7. Press "Enter" to create your local clone.

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://www.github.com/Ironmonkeynuts/tolkien_forum)

**Please Note**: in order to directly open the project in Gitpod, you should have the browser extension installed. A tutorial on how to do that can be found [here](https://www.gitpod.io/docs/configure/user-settings/browser-extension).

#### Forking

By forking the GitHub Repository, you make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original owner's repository. You can fork this repository by using the following steps:

1. Log in to GitHub and locate the [GitHub Repository](https://www.github.com/Ironmonkeynuts/tolkien_forum).
2. At the top of the Repository, just below the "Settings" button on the menu, locate and click the "Fork" Button.
3. Once clicked, you should now have a copy of the original repository in your own GitHub account!

### Local VS Deployment

There are no remaining major differences between the local version when compared to the deployed version online.

## Credits

### Content

| Source | Notes |
| --- | --- |
| [Markdown Builder](https://markdown.2bn.dev) | Help generating Markdown files |
| [Chris Beams](https://chris.beams.io/articles/git-commit) | "How to Write a Git Commit Message" |
| [I Think Therefore I forum](https://codeinstitute.net) | Code Institute walkthrough project inspiration |
| [Bootstrap](https://getbootstrap.com) | Various components / responsive front-end framework |
| [Cloudinary API](https://cloudinary.com) | Cloud storage for static/media files |
| [Whitenoise](https://whitenoise.readthedocs.io) | Static file service |
| [Python Tutor](https://pythontutor.com) | Additional Python help |
| [ChatGPT](https://chatgpt.com) | Help with code logic and explanations. Generated some sample articles. Created logo images and artwork |

### Media

| Source | Notes |
| --- | --- |
| [favicon.io](https://favicon.io) | Generating the favicon |
| [GPT-4o](https://chatgpt.com) | AI generated images |

### Acknowledgements

- I would like to thank my Code Institute mentor, [Tim Nelson](https://www.github.com/TravelTimN) for the support throughout the development of this project.
- I would like to thank my Runshaw College tutor, [Thomas Cowan](https://runshaw.ac.uk/) for the support throughout the development of this project.
- I would like to thank my Runshaw College classmates on the course for their support throughout the development of this project.
- I would like to thank the [Code Institute](https://codeinstitute.net) Tutor Team for their assistance with troubleshooting and debugging some project issues.
- I would like to thank the [Code Institute Slack community](https://code-institute-room.slack.com) for the moral support; it kept me going during periods of self doubt and impostor syndrome.
