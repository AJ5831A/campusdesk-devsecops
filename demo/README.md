# CampusDesk demonstration

Prepared for Aryan (AJ5831A). This campus IT variant credits the shared ResolveDesk implementation and uses its own category/location workflow, repository history and application evidence.

- [Narrated presentation video](presentation.mp4): all ten current slides, read by the MacBook’s Samantha voice.
- [PowerPoint presentation](presentation.pptx): 10 slides.
- [PDF presentation](slides.pdf): updated campus-specific content and final cleanup results.
- [Exact presenter script (PDF)](demo-script.pdf): printable word-for-word narration and actions.
- [Exact presenter script (Markdown)](demo-script.md): editable narration, local commands and evidence links.
- [Evidence index](evidence/README.md): actual local validation and separate deployment status.
- [Legacy walkthrough note](walkthrough.txt): points to the current script.

The presentation video reads the exact slide narration from the presenter guide using the synthetic macOS Samantha voice. It is not a recording of Aryan's own voice. The updated PDF, PowerPoint and video contain the final cleanup results.

[Watch the full walkthrough](walkthrough.mp4). It combines the current ten-slide presentation, an explicit historical-evidence disclosure, the actual recorded Git push and complete successful CI run, EKS application, Kubernetes resources, shared AWS Console captures, ArgoCD, Prometheus and corrected Grafana footage, followed by the final cleanup result. The cloud footage is preserved from the earlier real session; AWS is no longer running. AI assistance and shared-base credit remain disclosed.

The [presentation timing and narration](presentation-video.json) and [walkthrough section timings](walkthrough-video.json) identify durations and transitions. Both videos use H.264 with AAC audio. Generate the presentation with `python3 scripts/build-presentation-video.py` on macOS with FFmpeg and Poppler installed. The full assembly helper accepts the preserved runtime-prefix and corrected monitoring video paths: `python3 scripts/build-walkthrough-video.py /path/to/runtime-prefix.mp4 /path/to/monitoring.mp4`; it needs the reportlab dependency declared in `scripts/requirements.txt`. These are real recording inputs, not generated cloud footage.

Local verification passed 31 backend tests, four frontend tests, HTTP integration, restart persistence and browser checks for campus fields and mobile layout. The first complete CI run is [38900823423](https://github.com/AJ5831A/campusdesk-devsecops/actions/runs/38900823423).

Cloud deployment evidence uses the same temporary EKS infrastructure as ResolveDesk and is labelled as shared resources. CampusDesk application and database resources occupy their own namespace. Shared Terraform teardown completed with 59 resources destroyed; all 11 live cleanup checks passed. The KMS key is PendingDeletion until 15 November 2026. See the evidence index for the exact audit.
