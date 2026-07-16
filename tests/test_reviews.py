import pytest

from harness import reviews


def test_create_filter_and_delete_review(evals_dir):
    review = reviews.create_review(
        "run_1",
        "unacceptable",
        "missed options",
        "prompt_issue",
    )
    assert reviews.load_review(review.review_id) == review
    assert reviews.reviews_by_attribution("prompt_issue") == [review]
    reviews.delete_review(review.review_id)
    assert reviews.list_reviews() == []


def test_acceptable_review_has_no_change_target(evals_dir):
    review = reviews.create_review("run_1", "acceptable", "", "prompt_issue")
    assert review.failure_attribution is None
    assert review.status == "open"


def test_mark_review_used_hides_from_open_list(evals_dir):
    review = reviews.create_review("run_1", "unacceptable", "missed", "prompt_issue")
    reviews.mark_review_used(review.review_id, "prompt_v2")
    used = reviews.load_review(review.review_id)
    assert used.status == "used"
    assert used.used_by_version_id == "prompt_v2"
    assert used.used_at
    assert reviews.list_open_reviews() == []
    with pytest.raises(ValueError):
        reviews.delete_review(review.review_id)


@pytest.mark.parametrize("target", [None, "agent_failure", "ambiguous"])
def test_unacceptable_review_rejects_invalid_target(evals_dir, target):
    with pytest.raises(ValueError):
        reviews.create_review("run_1", "unacceptable", "bad", target)
