#!/usr/bin/env python3
"""
build_site.py
-------------
Generates a static wedding website (index.html + css/js/images) for
Adeola & Oluwaseun's wedding, in the style of estheranddaniel1226.com.

HOW TO USE
1. Make sure Python 3 is installed (no extra packages needed).
2. Edit the CONFIG dictionary below to change any text, dates, or which
   photo goes where (see static/images/ for the available filenames).
3. Run:  python3 build_site.py
4. Everything the site needs will be written to the `dist/` folder.
   Upload the *contents* of `dist/` to any static host:
   - Netlify (drag-and-drop the dist folder onto app.netlify.com/drop)
   - GitHub Pages
   - Your own hosting / cPanel `public_html`
5. Open dist/index.html directly in a browser to preview locally first.

RSVP NOTE
The site has no backend, so guests do not submit anything here. Instead the
RSVP section lists the people guests can message on WhatsApp to reserve a
seat, with a pre-filled message. See rsvp_couple_contacts and rsvp_contacts
below to change who is listed.
"""

import os
import re
import shutil
from datetime import datetime
from html import escape
from urllib.parse import quote

# ============================================================
# CONFIG: edit everything here, nothing else needs to change
# ============================================================

CONFIG = {
    "bride": "Adeola",
    "groom": "Oluwaseun",
    "bride_full": "Adeola Balogun",
    "groom_full": "Oluwaseun Solagbade",

    # Used for the live countdown: 24h format, site's local time
    "wedding_datetime_iso": "2027-01-30T12:00:00",
    "wedding_date_display": "30th January 2027",
    "wedding_time_display": "12:00 PM",

    "venue_name": "The La'ocassion Event Center",
    "venue_address": "55/57 Charity Road, off Social Club Road, "
                      "New Oko Oba / Abule Egba, Lagos State",

    "attire": "All white party",
    "colors_display": "Burgundy, Gold & White",

    "kids_note": "Please let us know if you'll be coming with your kids "
                 "so we can prepare adequately for them.",

    "how_we_met": (
        "It all started on the 14th of January 2021.\n\n"
        "I was heading back to Abeokuta after celebrating my dad's birthday "
        "when, on the bus, I spotted her and her sister. Of course, I "
        "immediately thought, \'Okay... I need this girl's number.\' 😂\n\n"
        "So I asked.\n\n"
        "She said NO 😭\n\n"
        "Now, a normal person might have taken the rejection and moved on. "
        "But apparently, I was not normal. 😂 I decided to find another route.\n\n"
        "Somehow, I got her to like one of my posts on Facebook, and let's "
        "just say... that little like became the beginning of a very "
        "interesting investigation. Before long, her number somehow found "
        "its way to me. 😌\n\n"
        "At the time, she was a 100-level student, so I played it cool. We "
        "became friends, talked, laughed, and slowly got closer.\n\n"
        "Then came June... and friendship officially became something more. ❤️\n\n"
        "I stayed by her side, watched her grow through school, and patiently "
        "waited until she finished her studies and settled into work. Then, "
        "five years after that first bus encounter, I finally asked the "
        "biggest question of my life: Will you be my wife? 💍\n\n"
        "And now, here we are.\n\n"
        "Funny how one bus ride, one rejected request for a phone number, and "
        "one Facebook like somehow led us here.\n\n"
        "Five years later, I guess that 'NO' was just the beginning of our "
        "YES. ❤️"
    ),

    "vow_groom": (
        "I want to marry Adeola Balogun because she genuinely loves God and "
        "has a sincere relationship with Christ, and I'm grateful that we "
        "share the same faith and desire to build a home centred on Him. "
        "I admire her convictions, values, kindness, and intentionality, as "
        "well as her desire to keep growing and becoming better.\n\n"
        "She is someone I can communicate with, build with, and face life "
        "alongside as a true partner. I love her heart, her character, her "
        "strength, her beautiful spirit, and yes, I love her beauty too. "
        "But beyond how she looks, I love the woman she is and the woman "
        "she is continually becoming in Christ. I believe we can build a "
        "marriage grounded in faith, love, truth, commitment, and choosing "
        "each other through every season."
    ),

    "vow_bride": (
        "I am choosing to do life with Oluwaseun Solagbade because he loves "
        "Jesus and genuinely desires to walk closely with Him, which is the "
        "most beautiful foundation I could ask for. He is faithful to what "
        "he believes God has called him to, has a beautiful and passionate "
        "soul, and cares deeply about the things and people he loves. I "
        "love how he complements me, notices and handles the things I "
        "often overlook, and brings strengths where I have weaknesses.\n\n"
        "Most importantly, he is teachable and committed to growth "
        "spiritually and in life, which is something I deeply value. So "
        "yes, we are two imperfect people committed to loving God, growing "
        "together, and making life beautiful for each other. And oh yes... "
        "he is a fine man too."
    ),

    # ---- Order of the day (edit times/titles freely; add or remove entries) ----
    "schedule": [
        {"time": "11:00 AM", "title": "Guest Arrival",
         "note": "Come early, find your seat, and settle in."},
        {"time": "12:00 PM", "title": "Wedding Ceremony",
         "note": "The vows, the rings, the whole thing."},
        {"time": "1:30 PM", "title": "Photos & Cocktails",
         "note": "Say cheese with the couple; drinks are on us."},
        {"time": "3:00 PM", "title": "Reception & Lunch",
         "note": "Time to eat, dance, and celebrate."},
        {"time": "5:00 PM", "title": "Cake Cutting & Toasts",
         "note": "Sweet words and sweeter cake."},
        {"time": "7:00 PM", "title": "Send-off",
         "note": "Wave us off as we begin forever."},
    ],

    "rsvp_deadline": "December 30th, 2026",
    "gift_deadline": "November 30th, 2026",

    # ---- RSVP contacts ----
    # Guests message one of these people on WhatsApp to reserve a seat.
    # country_code turns local numbers like 0816... into the international
    # format WhatsApp needs (234816...).
    "country_code": "234",
    # The couple's own numbers. Drop them in here and their cards appear
    # automatically; any entry without a phone is skipped.
    "rsvp_couple_contacts": [
        {"name": "Adeola", "phone": "09065497428", "relation": "The Bride"},
        {"name": "Oluwaseun", "phone": "08138415995", "relation": "The Groom"},
    ],
    "rsvp_contacts": [
        {"name": "Tosin", "phone": "08164288605", "relation": "Bride's Brother", "purpose": "directions"},
        {"name": "Omowunmi", "phone": "07043707011", "relation": "Groom's Sister", "purpose": "directions"},
    ],
    "contact_email": "solagbadeoluwaseun6@gmail.com",

    "wishlist_url": "https://wishgum.com/w/adecole",

    # ---- Image assignments ----
    # All files live in static/images/. Swap any filename below for a
    # different photo any time; nothing else needs to change.
    "images": {
        "hero": "traditional-close.jpg",
        "countdown_bg": "registry-full.jpg",
        "story": "gallery-8.jpg",
        "groom_portrait": "groom-solo-casual-bw.jpg",
        "bride_portrait": "bride-solo-studio-1.jpg",
        "gallery": [
            "registry-kiss-bw.jpg",
            "gallery-1.jpg",
            "registry-embrace.jpg",
            "gallery-9.jpg",
            "bride-solo-studio-2.jpg",
            "gallery-2.jpg",
            "registry-carry-bw.jpg",
            "gallery-10.jpg",
        ],
    },
}

# ============================================================
# HTML BUILDING: you shouldn't need to touch anything below
# ============================================================

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
IMAGES_DIR = os.path.join(HERE, "static", "images")


def img(name):
    return f"static/images/{CONFIG['images'].get(name, '')}"


def nl2br(text):
    return "</p><p>".join(text.strip().split("\n\n"))


def build_nav():
    initials = f"{CONFIG['bride'][0]} &amp; {CONFIG['groom'][0]}"
    links = [
        ("Our Story", "our-story"),
        ("Why", "why"),
        ("Ceremony", "details"),
        ("The Day", "the-day"),
        ("Gift Registry", "gifts"),
        ("RSVP", "rsvp"),
    ]
    panel_links = links + [("Gallery", "gallery")]
    nav_links = "\n".join(
        f'<a href="#{anchor}">{label}</a>' for label, anchor in links
    )
    panel_nav_links = "\n".join(
        f'<a href="#{anchor}">{label}</a>' for label, anchor in panel_links
    )
    return f"""
  <nav class="nav">
    <a class="monogram" href="#home">{initials}</a>
    <div class="nav-links">
      {nav_links}
    </div>
    <button class="menu-btn" aria-label="Open menu">&#9776;</button>
  </nav>
  <div class="menu-panel">
    <button class="menu-close" aria-label="Close menu">&times;</button>
    {panel_nav_links}
  </div>"""


def build_hero():
    return f"""
  <header class="hero" id="home">
    <img class="bg" src="{img('hero')}" alt="{CONFIG['bride']} and {CONFIG['groom']}">
    <div class="hero-content wrap">
      <div class="eyebrow">We're getting married</div>
      <h1>{CONFIG['bride']}<span class="amp">&amp;</span>{CONFIG['groom']}</h1>
      <div class="datestamp">{CONFIG['wedding_date_display']} <span>&bull;</span> {CONFIG['wedding_time_display']}</div>
    </div>
    <div class="scroll-cue"></div>
  </header>"""


def build_countdown():
    return f"""
  <section class="countdown-section">
    <div class="wrap">
      <div class="eyebrow">Counting down to forever</div>
      <h2>Save the Date</h2>
      <div class="cd-grid">
        <div class="cd-item"><div class="cd-num" id="cd-days">00</div><div class="cd-label">Days</div></div>
        <div class="cd-item"><div class="cd-num" id="cd-hours">00</div><div class="cd-label">Hours</div></div>
        <div class="cd-item"><div class="cd-num" id="cd-mins">00</div><div class="cd-label">Minutes</div></div>
        <div class="cd-item"><div class="cd-num" id="cd-secs">00</div><div class="cd-label">Seconds</div></div>
      </div>
    </div>
  </section>"""


def build_story():
    return f"""
  <section class="story" id="our-story">
    <div class="wrap">
      <div class="section-head">
        <div class="eyebrow">How it began</div>
        <h2>How We Met ❤️</h2>
        <div class="rule"></div>
      </div>
      <div class="story-flex">
        <div class="story-text">
          <p>{nl2br(CONFIG['how_we_met'])}</p>
        </div>
        <div class="img-col">
          <img src="{img('story')}" alt="{CONFIG['bride']} and {CONFIG['groom']}">
        </div>
      </div>
    </div>
  </section>"""


def build_vows():
    return f"""
  <section class="vows" id="why">
    <div class="wrap">
      <div class="section-head">
        <div class="eyebrow">Why we're doing this</div>
        <h2>In Their Own Words</h2>
        <div class="rule"></div>
      </div>
      <div class="vows-grid">
        <div class="vow-card">
          <img src="{img('groom_portrait')}" alt="{CONFIG['groom']}">
          <h3>{CONFIG['groom']}</h3>
          <div class="role">The Groom</div>
          <p>{nl2br(CONFIG['vow_groom'])}</p>
        </div>
        <div class="vow-card">
          <img src="{img('bride_portrait')}" alt="{CONFIG['bride']}">
          <h3>{CONFIG['bride']}</h3>
          <div class="role">The Bride</div>
          <p>{nl2br(CONFIG['vow_bride'])}</p>
        </div>
      </div>
    </div>
  </section>"""


def build_details():
    return f"""
  <section class="details" id="details">
    <div class="wrap">
      <div class="section-head">
        <div class="eyebrow">Join us</div>
        <h2>The Details</h2>
        <div class="rule"></div>
      </div>
      <div class="details-grid">
        <div class="detail-card">
          <h3>Venue</h3>
          <p><span class="accent">{CONFIG['venue_name']}</span><br>{CONFIG['venue_address']}</p>
        </div>
        <div class="detail-card">
          <h3>Attire</h3>
          <p><span class="accent">{CONFIG['attire']}</span><br>Colour theme: {CONFIG['colors_display']}</p>
        </div>
        <div class="detail-card">
          <h3>Kids</h3>
          <p>{CONFIG['kids_note']}</p>
        </div>
      </div>
    </div>
  </section>"""


def build_schedule():
    items = "\n".join(
        f"""      <li class="tl-item">
        <span class="tl-marker" aria-hidden="true"></span>
        <div class="tl-card">
          <div class="tl-time">{escape(e['time'])}</div>
          <h3>{escape(e['title'])}</h3>
          <p>{escape(e['note'])}</p>
        </div>
      </li>"""
        for e in CONFIG['schedule']
    )
    return f"""
  <section class="schedule" id="the-day">
    <div class="wrap">
      <div class="section-head">
        <div class="eyebrow">Order of the day</div>
        <h2>The Day</h2>
        <div class="rule"></div>
      </div>
      <ol class="timeline">
{items}
      </ol>
    </div>
  </section>"""


def build_gallery():
    photos = CONFIG['images']['gallery']
    tiles = "\n".join(
        f'<img src="static/images/{p}" alt="Gallery photo">'
        for p in photos
    )
    return f"""
  <section class="gallery" id="gallery">
    <div class="wrap">
      <div class="section-head">
        <div class="eyebrow">A few favourites</div>
        <h2>Gallery</h2>
        <div class="rule"></div>
      </div>
      <div class="gallery-grid">
        {tiles}
      </div>
    </div>
  </section>"""


def wa_link(phone, message):
    """Build a wa.me chat link from a local or international phone number."""
    digits = re.sub(r"\D", "", phone or "")
    if not digits:
        return ""
    code = CONFIG["country_code"]
    if digits.startswith("0") and len(digits) == 11:
        digits = code + digits[1:]
    elif len(digits) == 10 and not digits.startswith(code):
        digits = code + digits
    return "https://wa.me/" + digits + "?text=" + quote(message)


def _contact_message(person):
    if person.get("purpose") == "directions":
        return (f"Hi {person['name']}, could you please share directions to "
                f"the event hall for {CONFIG['bride']} & {CONFIG['groom']}'s "
                f"wedding on {CONFIG['wedding_date_display']}? Thank you.")
    return (f"Hi {person['name']}, I'd like to RSVP for "
            f"{CONFIG['bride']} & {CONFIG['groom']}'s wedding on "
            f"{CONFIG['wedding_date_display']}. My name is ")


def _person_card(person):
    phone = person.get("phone", "")
    link = wa_link(phone, _contact_message(person))
    button = ('<a class="wa-btn" href="' + escape(link) + '" target="_blank" '
              'rel="noopener">Chat on WhatsApp</a>') if link else ""
    return f"""      <div class="person-card">
        <div class="person-role">{escape(person.get('relation', ''))}</div>
        <div class="person-name">{escape(person['name'])}</div>
        <div class="person-phone">{escape(phone)}</div>
        {button}
      </div>"""


def build_rsvp():
    couple = [p for p in CONFIG['rsvp_couple_contacts'] if p.get('phone')]
    directions = [p for p in CONFIG['rsvp_contacts'] if p.get('phone')]
    couple_cards = "\n".join(_person_card(p) for p in couple)
    direction_cards = "\n".join(_person_card(p) for p in directions)
    return f"""
  <section class="rsvp" id="rsvp">
    <div class="wrap">
      <div class="eyebrow">You're invited</div>
      <h2>RSVP</h2>
      <p class="lead">We've reserved a seat just for you. Send a WhatsApp message to the bride or groom to RSVP. For directions to the event hall, contact Tosin or Omowunmi.</p>

      <div class="contact-group">
        <h3 class="contact-group-title">RSVP to the Couple</h3>
        <div class="rsvp-people">
{couple_cards}
        </div>
      </div>
      <div class="contact-group">
        <h3 class="contact-group-title">Event Hall Directions</h3>
        <div class="rsvp-people">
{direction_cards}
        </div>
      </div>
      <div class="rsvp-deadline">Kindly confirm by {CONFIG['rsvp_deadline']}</div>
    </div>
  </section>"""


def build_gifts():
    qr_src = (
        "https://api.qrserver.com/v1/create-qr-code/?size=240x240&color=5C0F26&bgcolor=FBF7F0&data="
        + CONFIG['wishlist_url'].replace(":", "%3A").replace("/", "%2F")
    )
    return f"""
  <section class="gifts" id="gifts">
    <div class="wrap">
      <div class="section-head">
        <div class="eyebrow">Not necessary, but...</div>
        <h2>Gifts</h2>
        <div class="rule"></div>
      </div>
      <p class="lead">
        But for those asking (and insisting!), we have a wishlist you can pick items from.
        We're also happy to receive a little help toward our future goals: our house fund,
        honeymoon fund, car fund, or however God might be leading you to support us.
      </p>
      <div class="gift-box">
        <img src="{qr_src}" alt="Scan to view our wishlist">
        <div class="gift-cta">
          <div>Scan the code, or tap below,<br>to view our wishlist.</div>
          <a class="btn" href="{CONFIG['wishlist_url']}" target="_blank" rel="noopener">View Our Wishlist</a>
        </div>
      </div>
      <p class="email-note">
        For our updated gift list, reach {CONFIG['groom']} directly:
        <a href="mailto:{CONFIG['contact_email']}">{CONFIG['contact_email']}</a><br>
        Please confirm by {CONFIG['gift_deadline']}
      </p>
    </div>
  </section>"""


def build_footer():
    return f"""
  <footer>
    <div class="display">{CONFIG['bride']} &amp; {CONFIG['groom']}</div>
    <div class="fine">{CONFIG['wedding_date_display']} &middot; Lagos, Nigeria</div>
  </footer>"""


def build_page():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{CONFIG['bride']} &amp; {CONFIG['groom']} | {CONFIG['wedding_date_display']}</title>
<meta name="description" content="Join {CONFIG['bride']} and {CONFIG['groom']} as they celebrate their wedding on {CONFIG['wedding_date_display']} at {CONFIG['venue_name']}, Lagos.">
<link rel="stylesheet" href="static/css/style.css">
</head>
<body data-wedding-datetime="{CONFIG['wedding_datetime_iso']}">
{build_nav()}
{build_hero()}
{build_countdown()}
{build_story()}
{build_vows()}
{build_details()}
{build_schedule()}
{build_gallery()}
{build_rsvp()}
{build_gifts()}
{build_footer()}
<script src="static/js/main.js"></script>
</body>
</html>"""


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    # copy static assets (css, js, images)
    shutil.copytree(os.path.join(HERE, "static"), os.path.join(DIST, "static"))

    # write the generated page
    html = build_page()
    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done. Open {os.path.join(DIST, 'index.html')} in a browser to preview,")
    print("or upload the contents of the dist/ folder to your host.")


if __name__ == "__main__":
    main()
