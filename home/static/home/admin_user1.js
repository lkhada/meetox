let $ = document

const deg = 6
const hr = $.querySelector("#hr")
const mn = $.querySelector("#mn")
const sc = $.querySelector("#sc")

setInterval(function(){
	let day = new Date()
	let hh = day.getHours() * 30
	let mm = day.getMinutes() * deg
	let ss = day.getSeconds() * deg

	//hr.style.transform = `rotateZ(${hh+(mm/12)}deg)`
	//mn.style.transform = `rotateZ(${(mm)}deg)`
	//sc.style.transform = `rotateZ(${(ss)}deg)`
	
	hr.style.transform = "rotateZ(" + (hh+(mm/12)) + "deg)"
	mn.style.transform = "rotateZ(" + mm + "deg)"
	sc.style.transform = "rotateZ(" + ss + "deg)"
})
