const SPIDER_HOST = 'spider';
const SPIDER_PORT = 8081;
const SPIDER_PREFIX_COURSE = '/course';

var request_course_head = (id) => {
    if (id === "" || id === undefined) {
        return 'http://' + SPIDER_HOST + ':' + SPIDER_PORT + SPIDER_PREFIX_COURSE;
    }
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
    .finally(() => {
        console.log("request finished")
    })
}

async function get_course_list(course_list) {
    await axios.get(request_course_head())
        .then((res) => {
            console.log(res.data)
        })
        .catch((err) => {
            console.log(err)
        })
        .finally(() => {
            console.log("course list got")
        })
}

const courses = [
    {
        "category": "计算机",
        "courses": [
            {
                "name": "计算系统基础",
                "id": "NJU-1002784001"
            },
            {
                "name": "嵌入式软件设计",
                "id": "DLUT-1002607070"
            },
            {
                "name": "数据结构",
                "id": "ZJU-93001"
            },
            {
                "name": "程序设计与算法（二）算法基础",
                "id": "PKU-1001894005"
            },
            {
                "name": " 面向对象程序设计——Java语言",
                "id": "ZJU-1001542001"
            },
            {
                "name": "C语言程序设计进阶",
                "id": "ZJU-200001"
            },
            {
                "name": "大数据计算技术",
                "id": "UESTC-1003037002"
            },
            {
                "name": "Python语言程序设计",
                "id": "BIT-268001"
            },
            {
                "name": "Office高级应用",
                "id": "CUIT-1002260004"
            },
            {
                "name": "Python数据分析与展示",
                "id": "BIT-1001870002"
            }
        ]
    },
    {
        "category": "外语",
        "courses": [
            {
                "name": "大学英语（口语）",
                "id": "NUDT-17004"
            },
            {
                "name": "初级汉语语法",
                "id": "BLCU-1002598041"
            },
            {
                "name": "大学英语II",
                "id": "ECJTU-1206603804"
            },
            {
                "name": "大学英语自学课程（下）",
                "id": "USTB-1001551007"
            },
            {
                "name": "大学英语自学课程（上）",
                "id": "USTB-299003"
            },
            {
                "name": "初级汉语口语",
                "id": "BNU-1002842008"
            },
            {
                "name": "日本文化解读",
                "id": "UESTC-1003043001"
            },
            {
                "name": "中国文化的日本之旅",
                "id": "JLU-1205723806"
            },
            {
                "name": "汉语国际教育概论",
                "id": "BLCU-1003467013"
            },
            {
                "name": "口译理论与实践",
                "id": "USTB-1206404811"
            }
        ]
    },
    {
        "category": "理学",
        "courses": [
            {
                "name": "高等数学（一）",
                "id": "NUDT-9004"
            },
            {
                "name": "流体流动与传热",
                "id": "CCZU-1001755188"
            },
            {
                "name": "文科高等数学",
                "id": "HUNNU-1205792813"
            },
            {
                "name": "城市环境地学",
                "id": "ECNU-1206633825"
            },
            {
                "name": "地球与人类文明",
                "id": "PKU-1206297809"
            },
            {
                "name": "高等数学—基本概念分析与理解",
                "id": "BJFU-1205913801"
            },
            {
                "name": "普通化学",
                "id": "TONGJI-45004"
            },
            {
                "name": "大学物理(上)",
                "id": "NWPU-1207120813"
            },
            {
                "name": "动物学",
                "id": "CCNU-1206692842"
            },
            {
                "name": "生理学（下）",
                "id": "PKU-1205937803"
            }
        ]
    },
    {
        "category": "工学",
        "courses": [
            {
                "name": "识图与制图",
                "id": "MYZYJS-1207169806"
            },
            {
                "name": "传质与分离工程",
                "id": "CCZU-1003444010"
            },
            {
                "name": "结构力学——超静定结构力学",
                "id": "HHU-1001755112"
            },
            {
                "name": "安全评价",
                "id": "CCZU-1207172801"
            },
            {
                "name": "系统设计创新与机器人实践",
                "id": "XJTU-1003365015"
            },
            {
                "name": "基础工程",
                "id": "SEU-1207041815"
            },
            {
                "name": "光纤光学",
                "id": "HUST-1206891801"
            },
            {
                "name": "电工电子技术实验（数字电子部分）",
                "id": "NEU-1206689824"
            },
            {
                "name": "电工电子技术实验（电路部分）",
                "id": "NEU-1206701814"
            },
            {
                "name": "材料力学",
                "id": "SDU-1206687825"
            }
        ]
    }
]
