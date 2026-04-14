# Cleaning Coordination System v1.0
**Created:** 2026-03-23 23:00 JST  
**Purpose:** Manage cleaning turnover between guest stays efficiently

## 🎯 SYSTEM OVERVIEW

### **Core Objectives:**
1. **Reliable Turnover:** Ensure property is always clean for next guest
2. **Quality Control:** Maintain consistent cleaning standards
3. **Cost Efficiency:** Optimize cleaning costs while ensuring quality
4. **Time Efficiency:** Minimize host time spent on cleaning coordination
5. **Scalability:** System that works for 1 to 10+ properties

### **Key Requirements:**
- 4-hour turnover window (check-out 11 AM, check-in 3 PM)
- Consistent quality across all cleanings
- Emergency cleaning capability for unexpected situations
- Cost control and performance tracking

## 👥 CLEANING OPTIONS

### **Option A: Professional Cleaning Service**
**Pros:**
- Consistent quality
- Insurance coverage
- Backup cleaners available
- Professional equipment/supplies

**Cons:**
- Higher cost (¥3,000-¥5,000 per cleaning)
- Less flexibility for last-minute changes
- May require minimum contract

### **Option B: Independent Cleaner**
**Pros:**
- Lower cost (¥2,000-¥3,500 per cleaning)
- More flexible scheduling
- Personal relationship possible

**Cons:**
- Single point of failure (if sick/unavailable)
- Quality may vary
- No insurance coverage

### **Option C: Hybrid Approach**
- Primary: Professional service for reliability
- Backup: Independent cleaner for emergencies
- Self-clean: For gaps or special situations

## 📋 CLEANING CHECKLIST

### **Standard Cleaning Tasks:**
**Bathroom:**
- [ ] Clean toilet inside and out
- [ ] Clean shower/bathtub
- [ ] Clean sink and mirror
- [ ] Wipe all surfaces
- [ ] Restock toilet paper (2 rolls)
- [ ] Restock soap/shampoo if provided
- [ ] Empty trash bin

**Kitchen:**
- [ ] Clean countertops
- [ ] Clean sink
- [ ] Clean stove/oven if used
- [ ] Clean microwave inside and out
- [ ] Clean refrigerator inside and out
- [ ] Empty trash bin
- [ ] Restock basic supplies (salt, oil, etc.)

**Living/Bedroom:**
- [ ] Vacuum all floors
- [ ] Mop hard floors
- [ ] Dust all surfaces
- [ ] Clean windows/mirrors
- [ ] Make beds with fresh linens
- [ ] Fluff pillows
- [ ] Empty trash bins

**General:**
- [ ] Check all lights working
- [ ] Check appliances functioning
- [ ] Restock supplies (toilet paper, trash bags, etc.)
- [ ] Verify WiFi working
- [ ] Test air conditioning/heating
- [ ] Check for any damage/maintenance issues
- [ ] Lock up and secure property

### **Deep Cleaning (Monthly):**
- [ ] Clean inside cabinets
- [ ] Clean behind appliances
- [ ] Wash curtains/blinds
- [ ] Clean air conditioner filters
- [ ] Clean balcony/outside areas
- [ ] Check smoke detector batteries

## 📅 SCHEDULING SYSTEM

### **Automated Scheduling:**
```
Guest checks out (11 AM) → Cleaning scheduled (11 AM - 2 PM) → Guest checks in (3 PM)
```

### **Tools for Scheduling:**
1. **Google Calendar:** Shared with cleaning service
2. **Airbnb Calendar Sync:** Auto-updates with bookings
3. **Cleaning Service App:** If service has own system
4. **Manual Spreadsheet:** Backup system

### **Communication Flow:**
```
1. Booking made → Calendar updated
2. Day before check-out → Cleaning reminder sent
3. Check-out confirmed → Cleaning service notified
4. Cleaning completed → Photo confirmation to host
5. Ready for next guest → Status updated in systems
```

## 💰 COST MANAGEMENT

### **Cost Structure:**
- **Standard Cleaning:** ¥3,000-¥4,000 per turnover
- **Deep Cleaning:** ¥5,000-¥7,000 (monthly)
- **Emergency Cleaning:** ¥4,000-¥6,000 (short notice)
- **Supply Restocking:** ¥500-¥1,000 per cleaning

### **Budgeting:**
```
Monthly Estimate (20 nights occupancy):
- 10 turnovers × ¥3,500 = ¥35,000
- 1 deep cleaning × ¥6,000 = ¥6,000
- Supplies × ¥800 × 10 = ¥8,000
- **Total Monthly:** ¥49,000
```

### **Cost Optimization:**
1. **Negotiate Volume Discount:** For multiple properties
2. **Supply Bulk Purchase:** Buy toilet paper, soap, etc. in bulk
3. **Efficient Scheduling:** Cluster bookings to reduce cleanings
4. **Quality vs Cost Balance:** Don't sacrifice quality for small savings

## 📊 QUALITY CONTROL

### **Inspection Methods:**
1. **Photo Verification:** Cleaner sends photos of each room
2. **Spot Checks:** Random in-person inspections
3. **Guest Feedback:** Monitor reviews for cleaning comments
4. **Checklist Completion:** Digital checklist submission

### **Quality Metrics:**
- **Guest Satisfaction:** 4.8+ rating for cleanliness
- **Issue Rate:** <5% of stays have cleaning complaints
- **Response Time:** <2 hours to address cleaning issues
- **Re-cleaning Rate:** <2% of cleanings need rework

### **Performance Tracking:**
| Cleaner | Date | Property | Score | Issues | Cost |
|---------|------|----------|-------|--------|------|
| Cleaner A | 2026-04-01 | Fukuoka #1 | 9/10 | None | ¥3,500 |
| Cleaner B | 2026-04-02 | Fukuoka #1 | 8/10 | Missed trash | ¥3,500 |
| Cleaner A | 2026-04-03 | Fukuoka #1 | 10/10 | None | ¥3,500 |

## 🚀 IMPLEMENTATION PLAN

### **Phase 1: Setup (Before First Guest)**
- [ ] Research and select cleaning service/cleaner
- [ ] Create detailed cleaning checklist
- [ ] Set up scheduling system (calendar)
- [ ] Establish communication protocol
- [ ] Purchase initial supplies

### **Phase 2: First Month Operation**
- [ ] Test with first few guests
- [ ] Refine checklist based on actual use
- [ ] Establish quality control process
- [ ] Negotiate terms with cleaner/service
- [ ] Set up backup cleaner

### **Phase 3: Optimization (Month 2-3)**
- [ ] Analyze costs and adjust as needed
- [ ] Implement performance tracking
- [ ] Scale system for additional properties
- [ ] Automate scheduling/communication further

## ⚠️ RISK MANAGEMENT

### **Common Risks:**
1. **Cleaner No-show:** Have backup cleaner on call
2. **Poor Quality:** Clear standards, photo verification, performance tracking
3. **Supply Shortage:** Maintain inventory, auto-reorder system
4. **Last-minute Booking:** Flexible cleaner or buffer day in pricing

### **Mitigation Strategies:**
- **Backup Cleaner:** Always have secondary option
- **Buffer Time:** Don't schedule back-to-back if possible
- **Supply Stock:** Keep 2x normal supply on hand
- **Insurance:** Ensure cleaner has liability insurance

## 🔄 SYSTEM INTEGRATION

### **Linked Systems:**
1. **Guest Management:** Check-out triggers cleaning schedule
2. **Calendar System:** Bookings auto-schedule cleanings
3. **Financial Tracking:** Cleaning costs tracked against budget
4. **Maintenance System:** Cleaners report issues found during cleaning
5. **Dashboard:** Real-time cleaning status and performance metrics

### **Automation Opportunities:**
1. **Auto-scheduling:** Calendar integration for automatic cleaning bookings
2. **Auto-payment:** Scheduled payments to cleaners
3. **Supply Monitoring:** Auto-reorder when supplies low
4. **Performance Alerts:** Notify if quality scores drop below threshold
5. **Guest Feedback Integration:** Auto-analyze reviews for cleaning mentions

## 📞 CLEANER COMMUNICATION TEMPLATES

### **Initial Contact (Japanese):**
```
件名: 福岡市での民泊清掃について

[Cleaner Name/Service] 様

初めまして。[Your Name]と申します。
福岡市で民泊（Airbnb）事業を開始するため、清掃サービスを探しています。

【ご依頼内容】
・民泊物件のチェックアウト後の清掃
・エリア: 福岡市（博多、天神、大名周辺）
・頻度: ゲストのチェックアウト後（月10-15回程度）
・時間: チェックアウト11時～チェックイン15時の間（4時間枠）
・内容: 標準清掃チェックリストに基づく清掃

【希望条件】
・信頼性の高い清掃品質
・緊急時対応可能
・写真による清掃確認
・責任保険加入

サービス内容と費用についてご相談させていただけますでしょうか。

よろしくお願いいたします。

[Your Name]
[Phone Number]
[Email]
```

### **Cleaning Confirmation Template:**
```
件名: 清掃予定確認 - [Property Name] [Date]

[Cleaner Name] 様

[Date]の清掃予定を確認させていただきます。

**物件:** [Property Name]
**住所:** [Address]
**チェックアウト:** 11:00 AM
**チェックイン:** 3:00 PM
**清掃時間:** 11:00 AM - 2:00 PM
**アクセス:** [Access instructions]

清掃完了後、各室の写真を送信いただけますと幸いです。
何か問題があれば、すぐにご連絡ください。

よろしくお願いいたします。

[Your Name]
```

---

**Next Update:** v1.1 after first cleaning experience  
**Owner:** Saito  
**Status:** READY - System designed and templates prepared  
**Implementation:** Can deploy immediately upon first property  
**Target:** <5 minutes/day per property cleaning coordination