# GitHub and demo guide

## 1. Keep the old project

Use the same repository and project board from Assessment 1. Do not make a new project. Download or clone the repository before making changes. Check which files already exist. Do not replace the old README, reminder tests or workflow without reviewing them; merge the relevant content instead. The new app uses `core.py` for reminders.

## 2. Review and add the files

Invite your approved group member to the repository and project board. Work together to check the draft against the seven existing story IDs. Use genuine feature work for branches and pull requests. For example, the team may split review and improvements into account access (US-01, US-02), pet profiles (US-03, US-04), and care and reminders (US-05, US-07, US-09). The team should decide who will do each task. Do not create fake commits or backdate work.

A simple way to add the initial draft is to make a branch named `feature/mvp-draft`, add the source files after review, open a pull request to `main`, ask the other member to review it, and merge it only when the checks pass. Use further real improvements on separate branches. Link actual issues or board items. Do not invent issue numbers. Add the release tag `v0.1.0-mvp` only once the reviewed version is ready.

## 3. Test and demonstrate

Use sample information only. Run the following steps on the staging site after it is deployed:

| Step | Action | Expected result |
|---|---|---|
| 1 | Register a sample account | Account is created; repeated email is rejected |
| 2 | Sign in with the correct details | Dashboard opens |
| 3 | Add Milo, a dog | Milo appears on the dashboard |
| 4 | Change Milo to Max | Updated name is saved |
| 5 | Add a vaccination with a care date two days ago and next due date yesterday | Record appears and is overdue |
| 6 | Add a clinic appointment for today or tomorrow | Appointment appears and is upcoming |
| 7 | Open the dashboard | Both reminders appear with the right labels |
| 8 | Sign out and open a private page | Redirects to sign in |
| 9 | Create a second sample account and try the first pet URL | The pet is not shown (404) |

Dates must be relative to the day you run the demo. The overdue and upcoming rules use Sydney time. Take screenshots of real results and keep the GitHub Actions run link. Use a screen recording as backup.

## 4. Evidence to collect for the report

- Staging site link and release tag.
- Real links to issues, pull requests, reviews and CI runs.
- Screenshots of the dashboard, pet profile and care/appointment records.
- Actual planned versus completed story status.
- Actual local, CI and manual test results.
- Genuine client or approved stakeholder feedback, including decisions and dates.
- Meeting notes, team contribution details and Sprint 2 UAT arrangements.

The brief sets Sprint 1 as 11–25 November 2026. Work carried out later must be recorded with its actual date. If the sprint goal was not reached by 25 November, describe the difference and any later progress separately. Ask the lecturer about late submission and the approved stakeholder if needed. The report must not claim that a client has agreed to changes before it happens.
