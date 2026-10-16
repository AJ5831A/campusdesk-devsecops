# CampusDesk demonstration

Prepared for Aryan (AJ5831A). This campus IT variant credits the shared ResolveDesk implementation and uses its own category/location workflow, repository history and application evidence.

- [PowerPoint presentation](presentation.pptx): 10 slides.
- [PDF presentation](slides.pdf): the same slide content.
- [Evidence index](evidence/README.md): actual local validation and separate deployment status.
- [Walkthrough narration and capture plan](walkthrough.txt).

[Watch the walkthrough video](walkthrough.mp4) (11 minutes 38 seconds, H.264 video with AAC audio). It presents all ten slides first, then records an actual Git push and complete successful CI run, the EKS application, Kubernetes resources, shared AWS Console captures, ArgoCD, Prometheus and live Grafana. The recording explicitly discloses synthetic narration and AI assistance.

Local verification passed 31 backend tests, four frontend tests, HTTP integration, restart persistence and browser checks for campus fields and mobile layout. The first complete CI run is [38900823423](https://github.com/AJ5831A/campusdesk-devsecops/actions/runs/38900823423).

Cloud deployment evidence uses the same temporary EKS infrastructure as ResolveDesk and is labelled as shared resources. CampusDesk application and database resources occupy their own namespace. Shared Terraform teardown completed with 59 resources destroyed; all 11 live cleanup checks passed. The KMS key is PendingDeletion until 15 November 2026. See the evidence index for the exact audit.
