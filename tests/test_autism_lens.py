import pytest

from backend.services.autism_lens import AutismLens


@pytest.fixture
def lens():
    """Fixture for the AutismLens."""
    return AutismLens()


def test_transform_simple_sentence(lens):
    """Task 5.2 Test: Test a simple sentence is transformed into a structured format."""
    text = "The system uses a database."
    result = lens.transform_context(text)

    assert "### 🎯 Main Point" in result
    assert "The system uses a database." in result
    assert "### 🔢 Key Details" not in result  # No extra details
    assert "### 📚 Definitions" not in result  # No definitions
    assert "### 🏁 Conclusion" in result


def test_transform_with_details(lens):
    """Task 5.2 Test: Test that sentences after the first are treated as details."""
    text = (
        "The API has three endpoints. The first is for users. The second is for data."
    )
    result = lens.transform_context(text)

    assert "### 🎯 Main Point" in result
    assert "The API has three endpoints." in result
    assert "### 🔢 Key Details" in result
    assert "1. The first is for users." in result
    assert "2. The second is for data." in result
    assert "### 🏁 Conclusion" in result
    assert "2 supporting detail(s)" in result


def test_transform_with_definitions(lens):
    """Task 5.2 Test: Test that 'is' and 'means' clauses are extracted as definitions."""
    text = "A Note is a unit of information. The CognitiveOrchestrator is the main service. An API means Application Programming Interface."
    result = lens.transform_context(text)

    assert "### 📚 Definitions" in result
    assert "- **Note**: a unit of information." in result
    assert "- **CognitiveOrchestrator**: the main service." in result
    assert "- **API**: Application Programming Interface." in result
    assert "3 definition(s)" in result


def test_transform_with_bullet_points(lens):
    """Task 5.2 Test: Test that existing bullet points are recognized as details."""
    text = "The system has several components. - A frontend UI. - A backend API. - A Cosmos DB database."
    result = lens.transform_context(text)

    assert "### 🔢 Key Details" in result
    assert "1. - A frontend UI." in result
    assert "2. - A backend API." in result
    assert "3. - A Cosmos DB database." in result
    assert "3 supporting detail(s)" in result


def test_transform_empty_and_whitespace_context(lens):
    """Task 5.2 Test: Test that empty or whitespace-only context is handled gracefully."""
    assert lens.transform_context("") == ""
    assert lens.transform_context("   \n\t   ") == "   \n\t   "


def test_full_transformation(lens):
    """Task 5.2 Test: Test a complex text with all components."""
    text = "The platform is a cognitive orchestrator. It has three main parts. - The API. - The AI service. - The database. A platform is a base for building applications."
    result = lens.transform_context(text)

    # Check for all sections
    assert "### 🎯 Main Point" in result
    assert "### 🔢 Key Details" in result
    assert "### 📚 Definitions" in result
    assert "### 🏁 Conclusion" in result

    # Check content
    assert "The platform is a cognitive orchestrator." in result
    assert "1. It has three main parts." in result
    assert "2. - The API." in result
    assert "- **platform**: a base for building applications." in result
    assert "3 supporting detail(s)" in result
    assert "1 definition(s)" in result
