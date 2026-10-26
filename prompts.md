# Prompts used to build these notebooks

This file records, in order, the user prompts that drove the creation of
`alexnet_demo.ipynb` and `efficientnet_demo.ipynb` in this directory, so the
session can be replicated. Status-check messages like "Check whether the
nbconvert execution finished..." are **excluded** — those were re-entry
prompts from the assistant's own background-task polling (`ScheduleWakeup`),
not things the user typed, and are not real prompts.

## Assistant model

All turns in this session were handled by **Claude Sonnet 5** (model id
`claude-sonnet-5`), via Claude Code. No model switch occurred mid-session.

(Separately, the *subjects* of the notebooks — the things being tested — are
torchvision's pretrained **AlexNet** (`AlexNet_Weights.IMAGENET1K_V1`) and
**EfficientNet-B0** (`EfficientNet_B0_Weights.IMAGENET1K_V1`). Not to be
confused with the assistant model above.)

## Budget / cost

From Claude Code's own `/exit` session summary:

```
Total cost:            $14.25
Total duration (API):  36m 22s
Total duration (wall): 3h 19m 17s
Total code changes:    888 lines added, 0 lines removed
Usage by model:
     claude-sonnet-5:  3.2k input, 152.9k output, 55.9m cache read, 381.9k cache write ($14.25)
    claude-haiku-4-5:  956 input, 12 output, 0 cache read, 0 cache write ($0.0010)
```

So: **$14.25** total, almost entirely `claude-sonnet-5` (a trace of
`claude-haiku-4-5` for a sub-$0.01 incidental task). Note the wall-clock time
above (3h19m) is *not* a complete picture either — this session's actual
end-to-end wall time, including the final 1000-step reruns, ran closer to
5 hours by the session's own clock; the API was only actively busy for 36
minutes of that, the rest being `jupyter nbconvert --execute` compute time
(further inflated by heavy CPU contention from other apps on the machine)
plus one run that stalled for roughly two hours before being killed and
diagnosed. Root cause of that stall: a `zoom()` helper resized a full image up
by the scale factor *before* cropping back down — at factor 3.0 on a
3000×4000 source photo that briefly materializes a ~108-megapixel
intermediate image. It was rewritten to crop first, then resize only the
final-size crop (fixed, and verified independently afterwards).

## Prompts, in order

1. **Initial setup** (`init`):
   > we will test here alexnet. use win cmd uv for env. make nb to load it and some random images as weel as imagenet off internet. do it in an nb - so we could see results. output should be prediction class (human readable over the image visual) as well as few misclassified examples

2. **Add the robustness-sweep cell**:
   > add a cell where for the same set of images we get 3 rows, where input image is transformed differently, and the gt class prob is shown for each of the transformed samples. use scale 30-300%, brightness 10-300%, and one of your choice. use log scale wrt identitiy.

3. **(sent while the above was in progress) Add the misclassified-optimization section**:
   > finally for all misclassified show 10 ims over 10 updates optimizing input to output correct class prediciton, and prist start and end correct class prob

4. **Add per-image transformed-sample grids**:
   > in addition to a plot for all we need images transformed with prob and params in ttl;

5. **(sent while the above was in progress) Clarify + increase optimization steps**:
   > we need not only prob plot but also image samples, in addition to one plot for all images - visualize transformed samples and write prob & params in title of each; optimisation needs way more steps. lets do 200, and show very 20th

6. **Question about the optimization objective**:
   > in optimisation, did you only maximize prob of correct class or also minimize other ones?

7. **Add diff columns to the optimization grid**:
   > add another 2 column showing difference between last optimized image and the initial one: with same color scale as the images (min0 max 1) and amplified from min to max range

8. **Add the EOT-style randomly-augmented optimization section**:
   > finally and another section with exactly same image optimisation as the current, with one difference - the input image is randomly augmented each step - random rescaling +-10%+crop, rotation up to 10 degree, random brightness, contrast, hue, and saturation +-10%

9. **Scale up optimization steps**:
   > lets change to 1000eps in both tests, and correspondingly plot every 100

10. **Save prompts to this file**:
    > finally save all my prompts to you into prompts.md, so anyone can replicate, also mention which models were uses, and budget spent

11. **Correct this file** (status-check entries wrongly attributed to the user):
    > "Check whether the nbconvert execution of alexnet_demo.ipynb finished; if so, verify outputs (no errors, images rendered including new EOT section with diff columns) and report to the user." and alike seem irrelevant and not my prompts

12. **(a follow-up correction sent while the above fix was in progress)**:
    > Reproducing from scratch has to be cleaned up too

13. **Add the EfficientNet notebook**:
    > add a second nb using efficientnet for exactly same tests, update docs accordingly.

## Reproducing from scratch

Given only this file and a clean `01_AlexNet` directory:

- Replaying prompts 1–9 in order against Claude Code with Sonnet 5 should
  reproduce `alexnet_demo.ipynb` as it stands.
- Prompt 13 then reproduces `efficientnet_demo.ipynb`: it's the exact same
  notebook structure and test sequence as `alexnet_demo.ipynb`, with only the
  model swapped (`alexnet`/`AlexNet_Weights` → `efficientnet_b0`/
  `EfficientNet_B0_Weights`) and the corresponding titles/labels updated —
  same images, same robustness sweep, same 1000-step optimization (plain and
  EOT-augmented) sections.

Prompts 10–12 are meta (about this file) and don't affect either notebook.

## Session 2 — EOT variance diagnosis and follow-up

A separate Claude Code session (same model, `claude-sonnet-5`), started fresh
against the state left by session 1 above.

From Claude Code's own session summary (final, as of the end of this
session — items 14–24 below):

```
Total cost:            $15.03
Total duration (API):  23m 4s
Total duration (wall): 1d 11h 19m
Total code changes:    759 lines added, 23 lines removed
Usage by model:
    claude-haiku-4-5:  972 input, 13 output, 0 cache read, 0 cache write ($0.0010)
     claude-sonnet-5:  3.0k input, 115.3k output, 35.1m cache read, 1.7m cache write ($15.03)
```

So: **$15.03** total, almost entirely `claude-sonnet-5` (a trace of
`claude-haiku-4-5` for a sub-$0.01 incidental task). The wall-clock time
above (1d 11h) reflects the session being left open/idle between turns, not
continuous work — the API was only actively busy for under 24 minutes;
separately, the two `jupyter nbconvert --execute` runs for the K=32 rerun
(~1h for AlexNet, ~2.5h for EfficientNet-B0) ran as background shell
processes outside the API-duration accounting above.

14. **Investigate the EOT section's weak effect**:
    > pls verify that image optimisation through augmentation is correct and
    > reasonable. even optimisation takes longer, the difference with input
    > is minimal and seemingly sperious, suggesting smth off. real model is
    > ofc super unstable at pixel level, but input augmentation is suppoed to
    > strongly regularize. to study it in depth - save images and the post
    > optimisation images, to study effect in details

    Diagnosis (not a code bug): gradients flow correctly through the
    augmentation pipeline and never saturate against the `clamp(0,1)`, but
    using a single random augmentation sample per step gives a very
    high-variance, nearly uncorrelated gradient direction step to step
    (cosine similarity ≈0.1 between consecutive steps, vs. ≈0.8 for plain
    ascent) — so the walk behaves like diffusion (`√N` progress) rather than
    directed ascent (`N` progress). Verified by comparing K=1 vs. K=8
    averaged samples/step on a reduced run.

15. **Apply the fix at full scale**:
    > pls set to 32 and rerun for both models the augmented one

    (mid-turn) > reme ber it WILL take long

    Set `N_AUG_SAMPLES = 32` (gradient averaged over 32 random augmentations
    per step) in both notebooks' EOT cell and reran each notebook fully via
    `jupyter nbconvert --execute --inplace` (~1h for AlexNet, ~2.5h for
    EfficientNet-B0, both CPU). Confirmed much stronger, smoother convergence
    across all misclassified images in both notebooks.

16. **Change the step display stride without rerunning**:
    > dont rerun but update code so that this out plot is generated in the
    > future, with another input column

    (mid-turn) > also save images at those epeiochs so can be reploted
    > withpout rerun

    `SNAPSHOT_EVERY` changed 100 → 200 in both notebooks; the optimization
    loops now also save every captured frame to
    `images/opt_study/frames/<stem>__<mode>__step<NNNN>.png` as a side
    effect, so a future replot never needs to rerun the optimization again.
    Both result-grid plotting cells gained an extra column: the initial
    (step 0) frame repeated right after the final step, for a direct
    start-vs-end comparison. Applied to the code only — per the request, the
    notebooks were *not* rerun, so their saved outputs still show the old
    11-column layout until next executed.

17. **Check this file is current**:
    > is the doc updated_

18. **Repo bookkeeping**:
    > lets make some bookkiping: 1. make a copy of current notebooks with
    > output *.ipynb -> *.results.ipynb ; all *results.ipynb will be big
    > files, so you have to use lfs for them. the *ipynb that are not results
    > should then (double check you dont delete important data) ckeared from
    > output; finally add readme description,  ensure to use ruff and what
    > else needed review and refactor the code;
    > ask for update usage values; after you receive them, finish, polish
    > and commit all

    (mid-turn) > also the script defined in pyproject shpuld somehow execute
    > all and populate both nb

    Made `alexnet_demo.results.ipynb` / `efficientnet_demo.results.ipynb` as
    output-carrying copies of the then-current notebooks, tracked via
    git-lfs (`*.results.ipynb` in `.gitattributes`); cleared outputs from the
    source `alexnet_demo.ipynb` / `efficientnet_demo.ipynb` in place.
    Discovered and fixed a pre-existing bug: the `01-alexnet` console script
    was broken (package dir `01_alexnet` is not a valid Python identifier,
    so the generated entry-point stub hit a `SyntaxError` on
    `from 01_alexnet import main`) — renamed the package to `alexnet_demos`
    and rewrote `main()` to actually execute both notebooks end to end via
    `nbclient` and write their `.results.ipynb` outputs, matching the
    bookkeeping split above. Added `ruff` as a dev dependency, fixed what it
    flagged (unsorted/unused imports; one `BLE001` explicitly ignored as
    intentional), and ran `ruff format`. Added this project's `README.md`.

19. **Publish**:
    > after commit = create public repo  and push; create another public
    > repo under dsl-unibe-ch with name CAS_AML_M4_Examples - and put
    > current repo as it's subrepo

    No `gh` CLI or credentials were available in the shell; installed
    `gh` via `winget`, the user completed `gh auth login` interactively.
    Created `neworldemancer/CAS_AML_M4_01_AlexNet` (public), pushed this
    repo to it as `origin`. Created `dsl-unibe-ch/CAS_AML_M4_Examples`
    (public; user is an active org member with repo-create rights) and
    added the above repo to it as a git submodule at path `01_AlexNet`.

20. **Fix references after a manual script rename**:
    > i have chanegs script name, please update what depends on it and push

    The user had renamed the `[project.scripts]` entry in `pyproject.toml`
    from `01-alexnet` to `run_all` directly (it had already slipped into
    the item-18/19 commit unnoticed). Updated the two `README.md`
    references to the old name and pushed.

21. **Emphasize the diff maps in the README**, across several short
    follow-ups in one turn:
    > also say that there are ready nbs
    > if you want ti just watch
    > emphasize in doc
    > that it's important to look at the difference optimized vs oiginal
    > with your own perception
    > and find what chanegd

    Added a callout near the top of `README.md` pointing at the
    `.results.ipynb` files for anyone who just wants to look, plus a
    paragraph telling the reader not to just glance at the final image but
    to inspect the raw/amplified diff maps themselves and judge whether the
    character of the change (not just its magnitude) differs between plain
    and EOT-regularized optimization.

22. **(ambiguous, clarified)**:
    > running the nb is done
    > and script is docen with clause help

    No output files had actually changed on disk at that point; asked the
    user to clarify what they meant before acting (avoided guessing at a
    multi-hour `run_all` execution on an ambiguous prompt).

23. **Clarification of 22**:
    > i meant you need to rsay in readme that there are already executed
    > result notebooks to study

    So item 21 above was the actual intent all along. Moved the callout to
    the very top of `README.md` (before the project description), sharpened
    its wording to state plainly that `.results.ipynb` are already executed
    and ready to study, and removed the now-redundant second callout further
    down the file.

24. **Final usage for this session**:
    > final usage of this secons ssession: Total cost: $15.03 [...]
    > (full block reproduced at the top of this section)
