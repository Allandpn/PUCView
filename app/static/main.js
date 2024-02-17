

document.addEventListener('DOMContentLoaded', async function () {
  const courses = await getDataAPI()
  formatPageCurrent(courses)
  changeNavHeight()
})

const getDataAPI = function () {
  let route = document.getElementById('route-state')
  return fetch(`/api/${route.textContent}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Erro de rede: ${response.status}`)
      }
      return response.json()
    })
    .catch((error) => {
      console.error('Erro na requisição:', error)
      return null
    })
}

const formatPageCurrent = function (courses) {
  var cards_course = document.getElementById('cards-course')
  var area = document.getElementById('project-area')
  var area_rubrics = document.getElementById('rubrics-area')
  let projects = ''
  let rubrics = ''
  let cards = ''

  if (courses !== null) {
    for (let course of courses) {
      if (course.is_project == false) {
        cards += setCardCourse(course, cards)
      } else {
        projects_rubrics = setProjectArea(course, projects)
        projects += projects_rubrics.content
        rubrics += projects_rubrics.rubrics
      }
    }
  }
  area.innerHTML = projects
  cards_course.innerHTML = cards
  area_rubrics.innerHTML = rubrics
  closeSpinner()
}

const setCardCourse = function (course, card) {
  let points_possible = 0
  let entered_score = 0
  let assignments = ''

  if (course.assignments.length > 0) {
    for (let assignment of course.assignments) {
      if (
        assignment.points_possible != null &&
        assignment.points_possible > 0 &&
        !assignment.assignment_name.includes('eavaliação') &&
        !assignment.assignment_name.includes('Revisão')
      ) {
        points_possible += assignment.points_possible
        entered_score += assignment.entered_score

        assignments += `
            
              <li class="list-group-item ">
              <a href="${assignment.html_url}" target="_blank" class="card-grade-item">
              <div class="row">
                <div class="col-md-8">
                <span>
                  ${assignment.assignment_name}:
                </span>
                </div>
                <div class="col text-center">
                  <span>
                    ${assignment.entered_score} / ${assignment.points_possible}
                  </span>
                </div>
              </div>
              </a>
              </li>
            
          `
      }
    }
  } else {
    points_possible = 100
    entered_score = 100
  }

  let course_grade = (entered_score / points_possible) * 100
  let hsl = `hsl(${course_grade * 1.2}, 70%, 80%)`

  let assignments_rubrics = `
      <div class="card m-3 p-0 shadow" style="width: 20rem">
        <div class="card-body">
          <a href="https://pucminas.instructure.com/courses/${course.course_id}" target="_blank">
            <div class="card-title">${course.course_name}</div>
          </a>
          <div class="progress">
            <div id="progress-bar-${course.course_id}" class="progress-bar" role="progressbar" style="width: ${course_grade}%; background-color: ${hsl}" aria-valuenow="${course_grade}" aria-valuemin="0" aria-valuemax="100">${course_grade}%</div>
          </div>
          <ul class="list-group list-group-flush mt-3">
              ${assignments}
          </ul>
        </div>
      </div>
    `

  return assignments_rubrics
}

const setProjectArea = function (course, area) {
  let points_possible = 0
  let entered_score = 0
  let assignments = ''
  let course_grade = 0
  let rubrics_ = ''

  for (let assignment of course.assignments) {
    assignments_cards = getAssignmentGrade(assignment, course.course_id)
    assignments += assignments_cards.assignments
    rubrics_ += assignments_cards.card
    let course_grade_data = getProjectGrade(assignment)
    points_possible += course_grade_data.points_possible
    entered_score += course_grade_data.entered_score
  }

  course_grade = (entered_score / points_possible) * 100
  const circumference = 40 * 3.142 * 1.85
  const dashoffset = circumference * (1 - course_grade / 100)

  var content = `
      <div class="card border-0 mt-4">
      <div class="card-body">
            <a href="https://pucminas.instructure.com/courses/${
              course.course_id
            }" target="_blank">
            <div class="card-title-project">${course.course_name}</div>
          </a>
        <div class="container-fluid card-project-grade mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewbox="0 0 100 100">
        <path class="grey" d="M40,90
                 A40,40 0 1,1 60,90"
              style="fill:none;"/>
        <path class="purple" d="M40,90
                 A40,40 0 1,1 60,90"
              style="fill:none; stroke-dashoffset:${dashoffset}"/>
              <text x="50" y="50" text-anchor="middle" alignment-baseline="middle" >${course_grade.toFixed(
                1
              )}%</text>
    </svg>
        
      </div class="mt-4">
      <ul class="list-group list-group-flush">
      ${assignments}
      </ul>
    </div>  
  `

  let accordion = `
  <p class="rubrics-title">Rúbricas do Projeto - ${course.course_name.slice(
    0,
    7
  )}</p>
  <hr>
  <div class="accordion" id="accordion${course.course_id}">
            ${rubrics_}
  </div>
  <p><p><p>
  `
  data = {
    content: content,
    rubrics: accordion,
  }

  return data
}

const getProjectGrade = function (assignment) {
  let points_possible = 0
  let entered_score = 0

  if (
    assignment.points_possible != null &&
    assignment.points_possible > 0 &&
    !assignment.assignment_name.includes('eavaliação') &&
    !assignment.assignment_name.includes('Revisão')
  ) {
    points_possible += assignment.points_possible
    entered_score += assignment.entered_score
  }

  data = {
    points_possible: points_possible,
    entered_score: entered_score,
  }

  return data
}

const getAssignmentGrade = function (assignment, course_id) {
  let entered_score_

  if (assignment.entered_score == 0 || assignment.entered_score == null) {
    entered_score_ = 0
  } else {
    entered_score_ = assignment.entered_score.toFixed(1)
  }

  let score_percent = (entered_score_ / assignment.points_possible) * 100

  let assignments = `
          
            <li class="list-group-item ">
            <a href="${assignment.html_url}" target="_blank" class="card-grade-item">
            <div class="row">
              <div class="col-md-9">
              <span>
                ${assignment.assignment_name}:
              </span>
              </div>
              <div class="col text-center">
                <span>
                  ${entered_score_} / ${assignment.points_possible}
                </span>
              </div>
            </div>
            </a>
            </li>
          
        `

  let rubrics_main = ''
  if (assignment.rubrics.length > 0) {
    let rubric_header = `
    <div class="card card-rubrics mb-2">
      <div class="card-header card-rubrics-header" id="heading${
        assignment.assignment_id
      }">
        <div class="mb-0 d-flex justify-content-between rubric-percent-content">
          <button
            class="btn btn-link button-collapse "
            type="button"
            data-toggle="collapse"
            data-target="#collapse${assignment.assignment_id}"
            aria-expanded=""
            aria-controls="${assignment.assignment_id}"
          >
            ${assignment.assignment_name}            
          </button>
          <span class="my-auto rubric-percent">${score_percent.toFixed(
            1
          )}%</span>
        </div>
        
      </div>
    `
    let rubrics_body = ''
    let rubrics = ''
    for (let rubric of assignment.rubrics) {
      rubrics += getRubricsGrade(rubric)
    }

    rubrics_body = `
    <div id="collapse${assignment.assignment_id}" class="collapse" aria-labelledby="heading${assignment.assignment_id}" data-parent="#accordion${course_id}">
      <div class="card-body list-group list-group-flush">
      ${rubrics}
      </div>
    </div>
    
  `

    rubrics_main = rubric_header + rubrics_body + `</div>`
  }
  data = {
    assignments: assignments,
    card: rubrics_main,
  }

  return data
}

const getRubricsGrade = function (rubric) {
  let description = rubric.description
  const long_description = rubric.long_description
  const point = rubric.point
  const tempElement = document.createElement('div')
  tempElement.innerHTML = long_description
  const long_description_ = tempElement.textContent

  const rubric_icon = {
    0: "<i class='fa fa-2x fa-battery-empty' style='color: #bd2f1c' ></i>",
    6: "<i class='fa fa-2x fa-battery-quarter' style='color: #cfcc12' ></i>",
    10: "<i class='fa fa-2x fa-battery-three-quarters' style='color: #2595e0' ></i>",
    12: "<i class='fa fa-2x fa-battery-full' style='color: #25e044' ></i>",
  }

  rubric_body = `
    
      <li class="list-group-item">
        <div class="row">
          <div class="col-md-10">
    ${long_description_}
          </div>
          <div class="col-md-2 text-center font-weight-bold my-auto">
          ${rubric_icon[point]}
          </div>
        </div>
      </li>
  `
  return rubric_body
}

const changeNavHeight = function () {
  let nav = document.getElementById('nav-menu-main')

  nav.style.height = '100%'
}



const closeSpinner = function () {
  var spinner = document.getElementById('spinner-content')
  spinner.style.display = 'none'
}