# CampusDesk demonstration

Prepared for Aryan (AJ5831A). This campus IT variant credits the shared ResolveDesk implementation and uses its own category/location workflow, repository history and application evidence.

- [PowerPoint presentation](presentation.pptx): 10 slides.
- [PDF presentation](slides.pdf): the same slide content.
- [Evidence index](evidence/README.md): actual local validation and separate deployment status.
- [Walkthrough narration and capture plan](walkthrough.txt).

The final walkthrough video is being prepared. It will disclose synthetic narration and show actual captured application and deployment evidence. A script or recording plan is not a completed video.

Local verification passed 31 backend tests, four frontend tests, HTTP integration, restart persistence and browser checks for campus fields and mobile layout. The first complete CI run is [38900823423](https://github.com/AJ5831A/campusdesk-devsecops/actions/runs/38900823423).

Cloud deployment and teardown evidence use the same temporary EKS infrastructure as ResolveDesk. They must be captured and labelled as shared resources; local screenshots alone do not prove them.
