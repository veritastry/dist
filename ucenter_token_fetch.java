




/** * 获取猎户签名 * 1:循环请求参数拼接成GET格式参数字符串 * 2:将client_secret拼接到字符串中 * 3:对拼接完成的字符串进行base64编码 * 4:对base64编码后的字符串进行MD5 * 6:最后将MD5转成小写 * * @param params       有序的参数map * @param clientSecret 用来加密的client_secret * @return 签名后的内容 */public static String getOrionSign(Map<String, String> params, String clientSecret) throws UnsupportedEncodingException {    StringBuilder paramsStr = new StringBuilder();    int index = 0;    for (Map.Entry<String, String> entry : params.entrySet()) {        if (0 != index) {            paramsStr.append("&");        }                          paramsStr.append(entry.getKey()).append("=").append(entry.getValue());        index++;    }// 拼接 appSecretparamsStr.append("&client_secret=").append(clientSecret);//base64String base64Sign = new String(Base64.getEncoder().encode(paramsStr.toString().getBytes()), "utf8");//MD5摘要并转小写String sign = MD5Util.MD5(base64Sign.getBytes());return sign.toLowerCase();}





/** To change this license header, choose License Headers in Project Properties.* To change this template file, choose Tools | Templates* and open the template in the editor.*/package com.orion.ucenter.common.util;import java.security.MessageDigest;/**** @author moonbird*/public class MD5Util {    public static String MD5(byte[] btInput) {        char hexDigits[]={'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};        try {            //byte[] btInput = s.getBytes();            // 获得MD5摘要算法的 MessageDigest 对象            MessageDigest mdInst = MessageDigest.getInstance("MD5");            // 使用指定的字节更新摘要            mdInst.update(btInput);            // 获得密文            byte[] md = mdInst.digest();            // 把密文转换成十六进制的字符串形式            int j = md.length;            char str[] = new char[j * 2];            int k = 0;            for (byte byte0 : md) {                str[k++] = hexDigits[byte0 >>> 4 & 0xf];                str[k++] = hexDigits[byte0 & 0xf];            }            return new String(str);        } catch (Exception e) {            return "";        }    }}





// 使用demopublic static void main(String[] args) throws UnsupportedEncodingException {//获取签名用的有序Map	Map<String, String> sortMap = getSortMap();//将请求参数放入有序Map中sortMap.put("A", "orion.ucenter.c6cbbd9daaa6425a");sortMap.put("B", "73f10983acbf33be24149c934b71fb34");//得到参数签名String sign = getOrionSign(sortMap, "a7ed11a4f93e4fa3963b4215fc0ed91f");System.err.println(sign);}




/** * 获取签名用的有序Map * 字典排序 * @return 有序Map */public static Map<String, String> getSortMap() {    return new TreeMap<>(String::compareTo);}