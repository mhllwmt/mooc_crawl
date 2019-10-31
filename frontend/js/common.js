const SPIDER_HOST = 'localhost';
const SPIDER_PORT = 8081;
const SPIDER_PREFIX_COURSE = '/course';

var request_course_head = (id) => {
    return 'http://' + SPIDER_HOST + ':' + SPIDER_PORT + SPIDER_PREFIX_COURSE + '/' + id;
}

async function get_course_by_id(id) {
    await axios.get(request_course_head(id))
    .then((res) => {
        console.log(res.data)
    })
    .catch((err) => {
        console.log(err)
    })
    .then(() => {
        console.log("request finished")
    })
}