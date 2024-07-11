// const uri = import.meta.env.VITE_API_URL;
export async function getContest(contestID, APIKey, secretKey) {
  const url = `/contests/${contestID}?key=${APIKey}&secret=${secretKey}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw response;
  }

  const data = response.json();
  return data;
}
export async function handlePostRequest(info, data) {
  const url = `/moodle_grades`;
  const body = {
    contest: {
      ...info,
      problems: info.problems.map((item, index) => {
        return {
          ...item,
          max_grade: parseFloat(data[`${index}`]),
          submissions: item.submissions.map((item) => {
            return {
              ...item,
              author_email: item.author.email,
            };
          }),
        };
      }),
    },
    legally_excused: [],
    late_submission_rules: {},
  };

  console.log("Post request body:", body);

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(body),
  });

  console.log("Server answer for file generating", response);

  if (response.status >= 500) {
    throw new Error("Something went wrong with CodeForces");
  } else if (!response.ok) {
    throw new Error("Something went wrong!");
  }
  return response;
}
