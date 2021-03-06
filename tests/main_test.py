from pytest import fixture
from blask import BlaskApp
import settings


class TestMain:

    testClient = None

    @fixture(autouse=True)
    def inittest(self):
        b = BlaskApp(
            templateDir=settings.templateDir,
            postDir=settings.postDir,
            defaultLayout=settings.defaultLayout,
            staticDir=settings.staticDir,
            title=settings.title,
        )
        b.app.testing = True
        self.testClient = b.app.test_client()

    def test_index(self):
        response = self.testClient.get("/")
        assert b"blask is a blogging engine" in response.data

    def test_page(self):
        response = self.testClient.get("/about")
        assert response.status_code == 200
        assert b"To use blask, you only need to edit" in response.data

    def test_nopage(self):
        response = self.testClient.get("/nopageerror")
        assert response.status_code == 200
        assert b"404" in response.data

    def test_search(self):
        response = self.testClient.post("/search", data=dict(search="about"))
        assert response.status_code == 200

    def test_tag_search(self):
        response = self.testClient.get("/tag/about")
        assert response.status_code == 200
        assert b"href='/about'" in response.data

    def test_category_search(self):
        response = self.testClient.get("/category/page")
        assert response.status_code == 200
        assert b"href='/about'" in response.data

    def test_author_search(self):
        response = self.testClient.get("/author/zerasul")
        assert response.status_code == 200
        assert b"href='/about'" in response.data

    def test_sub_page(self):
        response = self.testClient.get("/releases/sub2/test")
        assert response.status_code == 200
        assert b"subdirectory test" in response.data

    def test_get_sitemap(self):
        response = self.testClient.get("/sitemap.xml")
        assert response.status_code == 200
        assert b"<url><loc>http://localhost" in response.data
