import allure


@allure.feature("This is a Test Demo")
class TestDemo:
    @allure.story('打印测试')
    @allure.title('执行test_1')
    def test_1(self):
        print("hello jenkins!")

    @allure.story('打印测试')
    @allure.title('执行test_2')
    def test_2(self):
        a = "again"
        print(f"i am back! {a}")

    @allure.story('列表测试')
    @allure.title('执行测试用例test_3')
    def test_3(self):
        l = [1, 2, 3, 4, 5]
        print(l[-3:-1])
