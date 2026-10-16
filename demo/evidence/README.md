# CampusDesk evidence

This directory records the CampusDesk variant. Its campus category/location workflow and runtime checks are distinct from ResolveDesk. Shared AWS provisioning evidence will be identified explicitly rather than presented as a second cluster.

| Check | Artifact | Result |
|---|---|---|
| Backend validation and workflow | [local-pytest.txt](local-pytest.txt) | 31 tests passed |
| Frontend API handling | [local-frontend-tests.txt](local-frontend-tests.txt) | 4 tests passed |
| Real HTTP integration | [local-http-smoke.txt](local-http-smoke.txt) | CRUD, search, validation, statistics and metrics passed against local PostgreSQL |
| Container health | [local-compose-status.txt](local-compose-status.txt) | Local application services healthy |
| Browser workflow | [browser-check.json](browser-check.json) | Campus fields, editing, search, deletion, mobile visibility and overflow checks passed |
| Desktop queue | [application-desktop.png](application-desktop.png) | Synthetic campus tickets and category/location columns |
| Mobile queue | [application-mobile.png](application-mobile.png) | Full details and actions remain accessible |
| Ticket creation | [ticket-create.png](ticket-create.png) | Category selector and required campus location |

The first full CI run is [38900823423](https://github.com/AJ5831A/campusdesk-devsecops/actions/runs/38900823423). Its tested image source is `d9ce3f45394c19baa36a769c649a8deb06c54401`. Registry and CI reports are captured separately in this directory.

Local PostgreSQL persistence was verified by retaining a generated synthetic ticket, restarting PostgreSQL and the backend, fetching that ticket, and deleting it. Browser screenshots are actual local captures, not cloud deployment proof.

EKS workload, ArgoCD and live monitoring evidence is now captured below. Final shared teardown completed: 59 Terraform resources destroyed and all 11 live cleanup checks passed. The slide deck is in [../presentation.pptx](../presentation.pptx) and [../slides.pdf](../slides.pdf). The [full walkthrough](../walkthrough.mp4) uses disclosed synthetic narration over actual slides, UI and deployment evidence. [Video validation](video-validation.json) confirms H.264, AAC, 1440×900 and 698.31 seconds.

## Shared AWS console captures

[Shared VPC](shared-aws-vpc-console.png) and [shared EKS cluster](shared-aws-eks-console.png) are actual authenticated AWS Console screenshots from the common ResolveDesk/CampusDesk deployment session. The EKS console shows the shared cluster ACTIVE. These files refer to one shared cluster, not two separately provisioned environments. Namespace-specific CampusDesk workload and monitoring evidence remains separate.

Files produced by `scripts/render-evidence.py` display captured command output for readability. They are labelled evidence renderings and are not screenshots of the AWS Console or a live terminal. Application browser and AWS Console screenshots retain their actual source distinction.

## CampusDesk on the shared EKS cluster

- [Live ingress application](eks-ingress-application.png): actual campus namespace application with category and location fields.
- [Kubernetes resources](eks-campus-resources.txt) and [rendered command output](eks-campus-resources.png): two API replicas, two frontend replicas, completed migration, bound persistent storage and HPA.
- [ArgoCD browser capture](argocd-campus.png) and [status output](argocd-campus-status.txt): Synced, Healthy and Succeeded.
- [CampusDesk Prometheus targets](prometheus-campus-targets.png): two API endpoints UP.
- [Live Grafana dashboard](grafana-campus.png): populated request rate and p95 latency. The server-error panel has no matching series; this is not presented as a measured zero.
- [Shared Terraform plan](shared-terraform-plan.log) and [shared apply output](shared-terraform-apply.log): same infrastructure recovery session used by ResolveDesk.

The Grafana pod restarted during configuration, invalidating its earlier login session. The final video uses a fresh authenticated dashboard capture; the obsolete login scene is excluded.

## Video assembly

The authored slide segment is followed by actual runtime footage through 355.21424 seconds, then a fresh authenticated Grafana segment. The earlier dashboard login scene was excluded after a monitoring pod restart invalidated its session. [Timing evidence](video-edit-timing.json) records the source audio-segment durations used for this cut. The slide generator was corrected to CampusDesk branding; the obsolete inherited footer was masked only in the authored slide footage, never in runtime evidence.

The walkthrough itself triggers [CI run 38902732947](https://github.com/AJ5831A/campusdesk-devsecops/actions/runs/38902732947) for commit `c85837a512e8bc1a9866396632e2da2bd9c2d787` and records it through success. [Run metadata](video-ci-run.json) and [full log](video-ci-run.log) preserve the result. Image tags used for the deployment remain the separately verified `9a7a184c8b98d6ff99d13641073925bd81051066`.

## Terraform recovery status

The replacement EKS workers and both applications ran successfully, with actual namespace, ingress, GitOps and monitoring proof above. The recovery `terraform apply` did not finish successfully: it remained waiting for deletion of the failed original node group for about 21 minutes, then was gracefully interrupted with SIGINT, preserving its state and log. Terraform destroy was started afterward to remove the healthy temporary resources in parallel with the remaining failed-group cleanup. Final destroy completed with 59 resources removed; all 11 scoped live cleanup checks passed. The owned KMS key remains PendingDeletion until 15 November 2026, as required by AWS. Runtime success is not presented as a successful apply completion.

## Final shared cleanup

- [Terraform destroy summary](terraform-destroy-summary.txt) and [rendered output](terraform-destroy-summary.png): **59 resources destroyed**.
- [Live AWS audit](aws-cleanup-audit.json), [readable audit](aws-cleanup-audit.txt) and [rendered audit](aws-cleanup-audit.png): **all 11 scoped checks passed**, including terminated instances, deleted volumes, deleted EKS/VPC, no project network leftovers and empty Terraform state.
- [Recovery record](terraform-recovery-note.txt): exact quota recovery, interrupted apply and teardown handling.

The owned KMS key is scheduled for deletion on **15 November 2026**. This mandatory AWS waiting period is distinct from active compute or network infrastructure. Unrelated account resources were untouched. Both submissions share this one cleanup event.
