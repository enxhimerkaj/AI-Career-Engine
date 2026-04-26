import { useState } from "react";
import { useNavigate } from "react-router-dom";

const csSkills = [
  "Python",
  "JavaScript",
  "Java",
  "C#",
  "C++",
  "HTML",
  "CSS",
  "React",
  "Node.js",
  "Express.js",
  "SQL",
  "MySQL",
  "PostgreSQL",
  "MongoDB",
  "REST APIs",
  "Git",
  "GitHub",
  "Docker",
  "Linux",
  "AWS",
  "Azure",
  "Data Analysis",
  "Pandas",
  "NumPy",
  "Machine Learning",
  "TensorFlow",
  "Scikit-learn",
  "Flask",
  "FastAPI",
  "Cybersecurity",
  "Networking",
  "UI/UX",
  "Figma",
  "Testing",
  "Debugging",
];

function CareerForm() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    preferredJobTitle: "",
    highestEducationLevel: "",
    major: "",
    university: "",
    experienceTitles: [""],
    yearsOfExperience: "",
    currentSkills: [],
  });

  const [customSkill, setCustomSkill] = useState("");

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

  const toggleSkill = (skill) => {
    setFormData((prev) => {
      const alreadySelected = prev.currentSkills.includes(skill);

      return {
        ...prev,
        currentSkills: alreadySelected
          ? prev.currentSkills.filter((item) => item !== skill)
          : [...prev.currentSkills, skill],
      };
    });
  };

  const addCustomSkill = () => {
    const skill = customSkill.trim();

    if (!skill || formData.currentSkills.includes(skill)) {
      return;
    }

    setFormData((prev) => ({
      ...prev,
      currentSkills: [...prev.currentSkills, skill],
    }));

    setCustomSkill("");
  };

  const removeSkill = (skillToRemove) => {
    setFormData((prev) => ({
      ...prev,
      currentSkills: prev.currentSkills.filter((skill) => skill !== skillToRemove),
    }));
  };

  const handleCustomSkillKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addCustomSkill();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const cleanedData = {
      ...formData,
      experienceTitles: formData.experienceTitles.filter((title) => title.trim() !== ""),
      currentSkills: formData.currentSkills.filter((skill) => skill.trim() !== ""),
    };

    localStorage.setItem("careerFormData", JSON.stringify(cleanedData));
    navigate("/recommendations");
  };

  return (
    <div className="app">
      <div className="card form-card">
        <h1>Welcome to Career Engine AI</h1>

        <p className="subtitle">
          This tool is designed for <strong>computer science and tech careers</strong>.
          Fill out the form below and we’ll match you with relevant roles based on
          your target job, experience, skills, and education.
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

          <label>Experience Titles (optional)</label>
          {formData.experienceTitles.map((title, index) => (
            <div key={index} className="experience-row">
              <input
                type="text"
                placeholder="Example: Data Analyst Intern"
                value={title}
                onChange={(e) => handleExperienceChange(index, e.target.value)}
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
          <label>Years of Experience</label>
            <select
            name="yearsOfExperience"
            value={formData.yearsOfExperience}
            onChange={handleChange}
            required
            >
            <option value="">Select years of experience</option>
            <option value="0">No professional experience yet</option>
            <option value="1">Less than 1 year</option>
            <option value="2">1-2 years</option>
            <option value="3">3-4 years</option>
            <option value="5">5+ years</option>
            <option value="7">7+ years</option>
            <option value="10">10+ years</option>
            </select>

          <label>Skills</label>
          <p className="small-text">Select the skills you already have:</p>

          <div className="skills-grid">
            {csSkills.map((skill) => (
              <label key={skill} className="skill-option">
                <input
                  type="checkbox"
                  checked={formData.currentSkills.includes(skill)}
                  onChange={() => toggleSkill(skill)}
                />
                {skill}
              </label>
            ))}
          </div>

          <label>Add Extra Skill (optional)</label>
          <div className="skill-input-row">
            <input
              type="text"
              placeholder="Example: TypeScript, Power BI, Jira"
              value={customSkill}
              onChange={(e) => setCustomSkill(e.target.value)}
              onKeyDown={handleCustomSkillKeyDown}
            />

            <button
              type="button"
              className="secondary-btn"
              onClick={addCustomSkill}
            >
              Add Skill
            </button>
          </div>

          {formData.currentSkills.length > 0 && (
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
          )}

          <button type="submit" className="primary-btn">
            Find Matching Jobs
          </button>
        </form>
      </div>
    </div>
  );
}

export default CareerForm;