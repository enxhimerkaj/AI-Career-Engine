import { useState } from "react";
import { useNavigate } from "react-router-dom";

function CareerForm() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    preferredJobTitle: "",
    highestEducationLevel: "",
    major: "",
    university: "",
    experienceTitles: [""],
    currentSkills: [],
  });

  const [skillInput, setSkillInput] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleExperienceChange = (index, value) => {
    const updated = [...formData.experienceTitles];
    updated[index] = value;

    setFormData((prev) => ({
      ...prev,
      experienceTitles: updated,
    }));
  };

  const addExperienceField = () => {
    setFormData((prev) => ({
      ...prev,
      experienceTitles: [...prev.experienceTitles, ""],
    }));
  };

  const removeExperienceField = (index) => {
    const updated = formData.experienceTitles.filter((_, i) => i !== index);

    setFormData((prev) => ({
      ...prev,
      experienceTitles: updated.length ? updated : [""],
    }));
  };

  const addSkill = () => {
    const trimmed = skillInput.trim();
    if (!trimmed || formData.currentSkills.includes(trimmed)) return;

    setFormData((prev) => ({
      ...prev,
      currentSkills: [...prev.currentSkills, trimmed],
    }));
    setSkillInput("");
  };

  const removeSkill = (skillToRemove) => {
    setFormData((prev) => ({
      ...prev,
      currentSkills: prev.currentSkills.filter((skill) => skill !== skillToRemove),
    }));
  };

  const handleSkillKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addSkill();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    localStorage.setItem("careerFormData", JSON.stringify(formData));
    navigate("/recommendations");
  };

  return (
    <div className="app">
      <div className="card form-card">
        <h1>Welcome to Career Engine AI</h1>
        <p className="subtitle">
          Fill out the form below and we’ll match you with relevant jobs based on
          your target role, experience, skills, and education.
        </p>

        <form className="career-form" onSubmit={handleSubmit}>
          <label>Preferred Job Title</label>
          <input
            type="text"
            name="preferredJobTitle"
            placeholder="Example: Data Engineer"
            value={formData.preferredJobTitle}
            onChange={handleChange}
            required
          />

          <label>Highest Education Level</label>
          <select
            name="highestEducationLevel"
            value={formData.highestEducationLevel}
            onChange={handleChange}
            required
          >
            <option value="">Select education level</option>
            <option value="No degree">No degree</option>
            <option value="Associate">Associate</option>
            <option value="Bachelor">Bachelor</option>
            <option value="Master">Master</option>
            <option value="Doctorate">Doctorate</option>
          </select>

          <label>Major (optional)</label>
          <input
            type="text"
            name="major"
            placeholder="Example: Computer Science"
            value={formData.major}
            onChange={handleChange}
          />

          <label>University (optional)</label>
          <input
            type="text"
            name="university"
            placeholder="Example: National Louis University"
            value={formData.university}
            onChange={handleChange}
          />

          <label>Experience Titles</label>
          {formData.experienceTitles.map((title, index) => (
            <div key={index} className="experience-row">
              <input
                type="text"
                placeholder="Example: Data Analyst Intern"
                value={title}
                onChange={(e) => handleExperienceChange(index, e.target.value)}
                required={index === 0}
              />
              <button
                type="button"
                className="small-btn"
                onClick={() => removeExperienceField(index)}
              >
                Remove
              </button>
            </div>
          ))}

          <button
            type="button"
            className="secondary-btn"
            onClick={addExperienceField}
          >
            Add Another Experience Title
          </button>

          <label>Skills</label>
          <div className="skill-input-row">
            <input
              type="text"
              placeholder="Type a skill and press Enter or Add"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              onKeyDown={handleSkillKeyDown}
            />
            <button type="button" className="secondary-btn" onClick={addSkill}>
              Add Skill
            </button>
          </div>

          <div className="checkbox-group">
            {formData.currentSkills.map((skill) => (
              <div key={skill} className="checkbox-item">
                <span>{skill}</span>
                <button
                  type="button"
                  className="small-btn"
                  onClick={() => removeSkill(skill)}
                >
                  x
                </button>
              </div>
            ))}
          </div>

          <button type="submit" className="primary-btn">
            Find Matching Jobs
          </button>
        </form>
      </div>
    </div>
  );
}

export default CareerForm;