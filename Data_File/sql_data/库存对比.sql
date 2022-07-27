select distinct kc.WM_SP_BM,
                my_data.dbo.f_get_ycb(kc.WM_SP_BM) as dm
into #dmb
from GAIA_WMS_KUCEN kc;


select ykc.WM_SP_BM                                                   as goods_code,
       isnull(d.dm, ykc.WM_SP_BM)                                     as dym,
       pc.BAT_BATCH_NO                                                as batch_no,
       iif(ykc.wm_hwh = '33333' or ykc.WM_KCZT_BH = '1000', '1', '0') as zt,
       sum(ykc.WM_KCSL)                                               as kc_num,
       sum(ykc.WM_KYSL)                                               as ky_num,
       goods.PRO_NAME                                                 as goods_name,
       goods.PRO_SPECS                                                as specs,
       goods.PRO_UNIT                                                 as unit,
       goods.PRO_FACTORY_NAME                                         as factory_name
into #ydkc
from GAIA_WMS_KUCEN ykc
         left join GAIA_BATCH_INFO pc (nolock) on pc.BAT_PRO_CODE = ykc.WM_SP_BM and pc.BAT_BATCH = ykc.WM_PCH
         left join GAIA_PRODUCT_BUSINESS goods on goods.PRO_SELF_CODE = pc.BAT_PRO_CODE
         left join #dmb d on d.WM_SP_BM = ykc.WM_SP_BM
group by ykc.WM_SP_BM, isnull(d.dm, ykc.WM_SP_BM), pc.BAT_BATCH_NO,
         iif(ykc.wm_hwh = '33333' or ykc.WM_KCZT_BH = '1000', '1', '0'), goods.PRO_NAME, goods.PRO_SPECS,
         goods.PRO_UNIT, goods.PRO_FACTORY_NAME;


select yc.Goods_No,
       yc.Lot_No,
       iif(yc.Stock_Status = '1', '1', '0')                                                                     as zt,
       yc.Package_Unit,
       sum(yc.stock_quantity)                                                                                   as kc,
       sum(iif(yc.Package_Unit = 'kg' or yc.Package_Unit = N'千克', yc.stock_quantity * 1000, yc.stock_quantity)) as kcsl
into #yckc
from my_data.dbo.yc_kc yc
group by yc.Goods_No, yc.Lot_No, iif(yc.Stock_Status = '1', '1', '0'), yc.Package_Unit;

select d.goods_code      as '商品编号',
       c.goods_no        as '云仓编号',
       d.batch_no        as 'Y批号',
       c.Lot_No          as 'C批号',
       d.zt              as '药德状态',
       c.zt              as '云仓状态',
       d.kc_num          as 'Y数量',
       c.kcsl            as 'C数量',
       d.kc_num - c.kcsl as '库存差异',
       d.unit            as 'Y单位',
       c.Package_Unit    as 'C单位',
       c.kc              as '云仓原始库存',
       d.goods_name      as '商品名称',
       d.specs           as '规格',
       d.factory_name    as '厂家'
from #ydkc d
         left join #yckc c on c.Goods_No = d.dym and c.Lot_No = d.batch_no and c.zt = d.zt
where d.kc_num - c.kcsl <> 0
  and d.zt <> 0
order by d.goods_code;


drop table #dmb,#ydkc,#yckc
