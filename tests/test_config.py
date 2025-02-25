import pytest
from src.config.yx_config import YxConfig

@pytest.mark.unit
@pytest.mark.config
class TestYxConfig:
    """测试YxConfig配置类"""
    
    def test_config_attributes_exist(self):
        """测试配置类是否包含所有必需的属性"""
        assert hasattr(YxConfig, 'userName')
        assert hasattr(YxConfig, 'password')
        assert hasattr(YxConfig, 'autoLabel')
        assert hasattr(YxConfig, 'yxProductName')
        assert hasattr(YxConfig, 'autoPlanName')
        
    def test_config_types(self):
        """测试配置值的类型是否正确"""
        assert isinstance(YxConfig.userName, str)
        assert isinstance(YxConfig.password, str)
        assert isinstance(YxConfig.autoLabel, str)
        assert isinstance(YxConfig.yxProductName, str)
        assert isinstance(YxConfig.autoPlanName, str)
        
    def test_product_name_valid(self):
        """测试产品名称是否为有效值"""
        valid_products = [
            '01_BIOS',
            '02_BMC',
            '03_昆仑卫士',
            '04_机房管理系统'
        ]
        assert YxConfig.yxProductName in valid_products
        
    def test_auto_label_valid(self):
        """测试自动化标注方式是否为有效值"""
        valid_labels = [
            'autoType',
            'autoResult',
            'getPlanCase',
            'selectCase'
        ]
        assert YxConfig.autoLabel in valid_labels 