<template>
  <div class="payment-result-container">
    <h1>支付结果</h1>
    <div class="result-message" :class="{ success: paymentSuccessful, error: !paymentSuccessful }">
      {{ paymentSuccessful ? '支付成功！感谢您的支持。' : '支付失败，请重试或联系客服。' }}
    </div>
    <el-link type="primary" @click="go('/order/index')">回到订单页面</el-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from "vue-router";
import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { ElLoading } from 'element-plus'
import { getDate } from '@/utils/util.js'

const globalStore = GlobalStore();

const router = useRouter();


const paymentSuccessful = ref(true);

const updateOrder = async (ordernum) => {
  const orderdata = (await request('/ticketorder/index?tko_ordernumber='+ordernum)).data[0]
  await request('/ticketorder/update?id='+orderdata.id,{tko_status:3},'put')
 
}

const go = (url) => {
  router.push({path: url})
}



onMounted(async () => {
  const query = router.currentRoute.value.query
  const out_trade_no = query.out_trade_no; // 支付原始订单号
  const loading = ElLoading.service({
    lock: true,
    text: '支付状态查询中',
    background: 'rgba(0, 0, 0, 0.7)',
  })

  // 更新订单状态
  await updateOrder(out_trade_no)
   loading.close()
});
</script>

<style scoped>
.payment-result-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80vh;
  flex-direction: column;
}

.result-message {
  font-size: 18px;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
}

.success {
  background-color: #4caf50;
  color: #fff;
}

.error {
  background-color: #f44336;
  color: #fff;
}
</style>